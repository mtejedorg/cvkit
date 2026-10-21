import os
import sys
import glob
import markdown
import subprocess

try:
    from pdf_crop import crop_pdf_to_content
except ImportError as exc:
    raise ImportError(
        "pdf_crop.py (and its dependency PyMuPDF/fitz) is required to compile PDFs. "
        "Run: pip install PyMuPDF"
    ) from exc

import tempfile
from pathlib import Path

# Output folders live in <repo>/_generated/<FolderName>/ (override with CV_OUTPUT_DIR).
root_dir = os.environ.get('CV_OUTPUT_DIR', str(Path(__file__).resolve().parent / '_generated'))


def find_edge():
    candidates = [
        os.environ.get('EDGE_PATH'),
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
        '/usr/bin/microsoft-edge',
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    raise SystemExit('Microsoft Edge not found. Set EDGE_PATH to your msedge executable.')


edge_path = find_edge()

if not os.path.isdir(root_dir):
    raise SystemExit(f'Output folder not found: {root_dir}. Create _generated/<FolderName>/ with your Markdown files first.')

# Rendered deliberately taller than any real CV/cover letter/portfolio can
# reach, so content never overflows to a second page. pdf_crop.py then trims
# the page down to the actual content height after rendering - see that
# module for why a fixed oversized bound + post-crop replaced the old
# per-line height estimate (it consistently overestimated and left large
# trailing whitespace at the bottom of the page).
OVERSIZED_PAGE_HEIGHT_MM = 2000

html_template = '''
<!DOCTYPE html>
<html>
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --primary: #2563eb;
    --text-main: #1f2937;
    --text-light: #4b5563;
    --bg-color: #ffffff;
    --accent: #eff6ff;
  }
  @page { 
    size: 210mm {page_height}mm; /* Continuous single-page layout fitted to content */
    margin: 15mm 20mm; 
  }
  body { 
    font-family: 'Inter', sans-serif; 
    color: var(--text-main); 
    line-height: 1.6; 
    font-size: 11pt;
    margin: 0;
    padding: 0;
  }
  /* Flexbox Header Layout */
  .cv-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 16px;
    margin-bottom: 24px;
  }
  .cv-header-text {
    flex: 1;
  }
  .cv-header-text h1 {
    color: #111827; 
    font-size: 24pt; 
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
    margin-top: 0;
    text-transform: uppercase;
  }
  .cv-header-text p {
    color: var(--text-light);
    font-size: 10pt;
    margin: 0;
  }
  /* Fallback for simple h1 */
  h1:not(.cv-header-text h1) { 
    color: #111827; 
    font-size: 24pt; 
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
    margin-top: 0;
    text-transform: uppercase;
  }
  h1:not(.cv-header-text h1) + p { 
    color: var(--text-light);
    font-size: 10pt;
    margin-top: 0;
    margin-bottom: 24px;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 16px;
  }
  h2 { 
    color: var(--primary); 
    font-size: 14pt; 
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 24px; 
    margin-bottom: 12px;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 4px;
  }
  p { margin-top: 6px; margin-bottom: 6px; color: var(--text-light); }
  strong { color: var(--text-main); font-weight: 600; }
  ul { 
    padding-left: 18px; 
    margin-top: 6px;
    margin-bottom: 16px;
  }
  li { 
    font-size: 10.5pt; 
    margin-bottom: 6px; 
    color: var(--text-light);
    padding-left: 4px;
  }
  li::marker { color: var(--primary); }
  a { color: var(--primary); text-decoration: none; }
  p > strong:first-child { font-size: 12pt; color: #111827; }
  em { font-style: normal; color: #6b7280; font-size: 9.5pt; font-weight: 500; }
  
  h1, h2, h3 { 
    page-break-after: avoid; 
    break-after: avoid; 
  }
  ul, p, li, .experience-block { 
    page-break-inside: avoid; 
    break-inside: avoid; 
  }

  .profile-photo {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--accent);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-left: 20px;
    flex-shrink: 0;
  }
</style>
</head>
<body>
{content}
</body>
</html>
'''

excluded_dirs = {'.git'}

# Target a folder via command-line argument; "Acme" and "_generated/Acme" both work.
args = [a for a in sys.argv[1:] if a != "--force"]
target_filter = os.path.basename(os.path.normpath(args[0])) if args else None
force_recompile = "--force" in sys.argv

for root, dirs, files in os.walk(root_dir):
    dirs[:] = [d for d in dirs if d not in excluded_dirs]
    if root == root_dir:
        continue
        
    # If a specific folder target is requested, skip non-matching directories
    if target_filter and target_filter.lower() not in root.lower():
        continue
        
    for file in files:
        if file.endswith('.md'):
            md_path = os.path.join(root, file)
            html_path = os.path.join(root, file.replace('.md', '.html'))
            pdf_path = os.path.join(root, file.replace('.md', '.pdf'))
            
            # Incremental build check: skip if PDF exists and is newer than MD file (unless target_filter or force_recompile is specified)
            if not force_recompile and not target_filter and os.path.exists(pdf_path):
                if os.path.getmtime(pdf_path) >= os.path.getmtime(md_path):
                    continue

            
            with open(md_path, 'r', encoding='utf-8') as f:
                md_text = f.read()
                
            calc_height = OVERSIZED_PAGE_HEIGHT_MM

            html_content = markdown.markdown(md_text)
            full_html = html_template.replace('{page_height}', str(calc_height)).replace('{content}', html_content)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
                
            import pathlib, time
            html_uri = pathlib.Path(html_path).resolve().as_uri()
            abs_pdf_path = os.path.abspath(pdf_path)
            temp_profile = os.path.join(tempfile.gettempdir(), 'edge_headless_pdf')
            msedge_cmd = [
                edge_path,
                '--headless',
                '--disable-gpu',
                '--no-pdf-header-footer',
                f'--user-data-dir={temp_profile}',
                f'--print-to-pdf={abs_pdf_path}',
                html_uri
            ]
            try:
                subprocess.run(msedge_cmd, check=True, timeout=20)
                time.sleep(1)
                print(f'Successfully compiled: {abs_pdf_path}')
                try:
                    final_height = crop_pdf_to_content(abs_pdf_path)
                    print(f'  Cropped to {final_height:.1f}mm content height')
                except Exception as crop_err:
                    print(f'  Warning: could not crop {abs_pdf_path}: {crop_err}')
            except Exception as e:
                print(f'Error compiling {abs_pdf_path}: {e}')
            
            if os.path.exists(html_path):
                os.remove(html_path)




