# Capturing real screenshots

Captures are the one step a session cannot finish alone: somebody has to run the software and reach the interesting screens. The helper below makes the saving part one keypress, so the user can do a pass in a few minutes.

## Unity

Add an Editor script (ask first; it is the only project file the skill touches outside the site folder):

```csharp
// Assets/Editor/SiteCapture.cs
using UnityEditor;
using UnityEngine;

public static class SiteCapture
{
    [MenuItem("Tools/Site/Capture 1920x1080 %#k")]
    public static void Capture()
    {
        System.IO.Directory.CreateDirectory("Captures/site");
        var path = $"Captures/site/{System.DateTime.Now:yyyyMMdd_HHmmss}.png";
        ScreenCapture.CaptureScreenshot(path, 1);
        Debug.Log($"Saved {path}");
    }
}
```

Set the Game view to 1920×1080 before pressing Ctrl+Shift+K in Play mode. If the repo already has a `Captures/` folder with real gameplay, prefer those and skip the helper.

## Godot 4

Add a debug-only autoload (ask first), excluded from release builds through a feature check:

```gdscript
# addons/site_capture/site_capture.gd  (autoload name: SiteCapture)
extends Node

func _input(event: InputEvent) -> void:
    if OS.has_feature("release"):
        return
    if event is InputEventKey and event.pressed and event.keycode == KEY_F12:
        var dir := "user://site_captures"
        DirAccess.make_dir_recursive_absolute(dir)
        var path := "%s/%s.png" % [dir, Time.get_datetime_string_from_system().replace(":", "-")]
        get_viewport().get_texture().get_image().save_png(path)
        print("Saved ", ProjectSettings.globalize_path(path))
```

Run with `godot --path .`, press F12 on each screen, then copy the files out of the user data folder (the print shows the absolute path).

## Web, desktop or CLI projects

Use the browser's device toolbar at 1920×1080 and the OS screenshot tool; for a CLI, a terminal capture at a readable font size is a real capture too.

## Choosing

- The preview is the single frame a stranger would understand in one second. Mid-use beats a menu.
- At least one capture per deep page (mechanics, tech): the tech page can show a profiler, an editor view or a diagram drawn from the real architecture, labelled as a diagram.
- Never a concept render, mockup or AI image as a capture. If that is all the repo has, the site ships with a "Concept art" section and no preview, and the manifest says so in the blurb.
