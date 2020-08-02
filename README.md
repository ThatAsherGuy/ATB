# Asher's Toolbox

Asher's Toolbox (ATB) is a Blender add-on that re-shuffles and re-wraps existing Blender features, aiming to speed up common tasks without enforcing a particular workflow or overloading the user's keymap.

## Main Interfaces

ATB is, at its core, a pile of interfaces. Here are the main ones you'll interact with:

### In The Sidebar: The Overlays Panel

![ATB Overlays Panel](https://i.imgur.com/SMJmaBR.png)

The overlays panel is a more-or-less straight remix of the shading and overlay popovers in the viewport header, with a few object display and theme settings thrown in for good measure. This panel has been designed to work with a fairly narrow column width, which makes it great for situations where you're toggling overlays off and on and you don't want to deal with popovers.

### In The Keymap: The Fast Panel

![ATB Fast Panel](https://i.imgur.com/6Yocaox.png)

Think of the fast panel as a compact one-stop-shop for object display settings. It's great for controlling things like the display mode of Boolean cutters, geometry data overlays, and x-ray shading.

While the fast panel does have a few tabs for future features, those tabs haven't been filled yet.

### In The Viewport Header: The Meta Panel

![ATB Meta Panel](https://i.imgur.com/oQtCxAF.png)

The meta panel splits the difference between the overlays panel and the fast panel. It's more compact than the former, but more exhaustive than the latter, providing convenient access to transform settings, a camera manager, viewport shading, and active object properties.

The camera manager and the active object panel are currently the most feature-rich, with the former offering easy access to your scene's camera list, camera settings, and a handful of keying options, and the latter exposing contextual properties for meshes, curves, lights, probes, and so on.
