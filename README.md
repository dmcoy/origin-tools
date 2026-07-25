# Origin Tools

A powerful Blender add-on for efficiently manipulating object origins, aligning mesh geometry, and correcting coordinate axis orientation.

![Origin Tools Panel](readme_images/origin-tools-panel.png)

## About This Add-on

Origin Tools streamlines common origin-related tasks in Blender, making it easier to:
- Set object origins to specific locations (geometry, cursor, 3D cursor, center of mass)
- Reorient local axes without affecting world position
- Automatically align mesh geometry to correct axis orientation using RANSAC algorithm

Perfect for artists and modelers who frequently work with imported or procedurally generated meshes that may have incorrect origin placement or axis orientation.

## Installation

### From GitHub Release (Recommended)

1. Download the latest `.zip` file from the [Releases page](https://github.com/dmcoy/origin-tools/releases)
2. Open Blender and go to **Edit > Preferences > Add-ons**
3. Click the **"Install..."** button in the top-right corner
4. Navigate to and select the downloaded `.zip` file
5. The add-on will now appear enabled by default

### From Disk

1. Place the extracted `origin_tools/` folder in your Blender add-ons directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\<version>\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/<version>/scripts/addons/`
   - **Linux**: `~/.config/blender/<version>/scripts/addons/`
2. Restart Blender
3. Enable the add-on in **Preferences > Add-ons** (search for "Origin Tools")

## Usage

### Accessing the Panel

The Origin Tools panel is located in the 3D Viewport sidebar:
1. Press `N` to toggle the sidebar if it's not visible
2. Click on the **"Item"** category tab to reveal the Origin Tools panel

### Basic Requirements

- At least one object must be selected to use any operation
- The add-on works in both **Object Mode** and **Edit Mode** (except "Set origin to selection")
- For mesh alignment features, ensure your active object is a mesh type

## Features

### Change Origin Orientation

Rotate the local coordinate system of selected objects while preserving their world position and rotation. This can be useful for swapping origin axes around (e.g., swapping the Z for Y axis).

![Change Orientation](gifs/change_orientation.gif)

**Use Cases:**
- Converting between Z-up and Y-up coordinate systems (e.g., Maya to Blender)
- Adjusting axis orientation without losing object placement
- Correcting models imported from different software with conflicting conventions

**How It Works:**
- Select an object and ensure your desired rotation angle is set in the panel
- Click + or - for X, Y, or Z axes to rotate the origin accordingly
- The mesh geometry transforms inversely to maintain world alignment

---

### Set Origin Options

Quickly set the origin of selected objects to various reference points. Each operation applies to all currently selected objects.

![Set Origin](gifs/set_origin.gif)

#### Origin to Geometry
Sets each object's origin to the geometric center (median) of its mesh data. Ideal for imported models with irregular geometry distribution.

#### Geometry to Origin
Moves all mesh geometry so it radiates from the current origin position. Useful when you've manually placed an origin point and want everything relative to it.

#### Origin to 3D Cursor
Sets the origin to the exact location of your 3D cursor. Perfect for placing origins at specific reference points or pivot locations.

#### Origin to Mass (Surface)
Calculates the center of mass based only on surface area (2D approximation). Faster than volume calculation, suitable for thin objects and sheets.

#### Origin to Mass (Volume)
Computes the true center of mass by analyzing the entire mesh volume. Most accurate for 3D objects but requires more computation time.

#### Set Origin to Selection *(Edit Mode Only)*
Sets the origin based on selected vertices in edit mode. Requires being in Edit Mode and selecting specific vertices. The 3D cursor is automatically reset to world origin after execution.

![Set Origin to Selection](gifs/set_origin_to_selection.gif)

---

### Align Origin Tools

Automatically align mesh geometry with its dominant axis orientation using advanced RANSAC (Random Sample Consensus) algorithm for robust estimation.

> [!WARNING]
> This is an experimental feature and may not work effectively depending on the mesh's geometry. Results may vary based on mesh complexity, symmetry, and structure.

#### Object to Origin
Aligns the mesh geometry so it's centered around its current origin position. Useful when you have an object properly positioned but its geometry needs centering relative to that pivot point.

#### Origin to Object
Reorients the object's origin and local axes to match the dominant orientation of the mesh geometry. This is particularly useful for:
- Fixing models imported with incorrect axis orientation (e.g., X-up instead of Z-up)
- Correcting twisted or rotated meshes from CAD software
- Standardizing axis conventions across different modeling tools

**How It Works:**
1. The algorithm analyzes polygon normals and areas to determine the dominant axes
2. Uses RANSAC for robust outlier rejection (handles imperfect geometry well)
3. Applies rotation transformation to align with standard cardinal directions

![Align Origin to Object](gifs/align_origin_to_object.gif)

---

## Requirements

- **Blender**: Version 4.2.0 or later

## License

This add-on is released under the **GNU General Public License v3.0 or later**.
See [LICENSE](LICENSE) for details.

### Important GPL Notice

When distributing modified versions of this add-on:
- You must include the complete source code
- You must retain all copyright notices and license text
- You must make the source available to recipients at no additional cost
- Consider releasing your modifications back to the community

## Changelog

### Version 1.0.0 (Current)
- **Major Release**: Ready for Blender Extensions Platform submission
- Complete module restructuring for clarity and maintainability
- Refined mesh alignment algorithm with improved accuracy
- Fixed numerical issues in rotation transformation calculations
- Comprehensive documentation and code comments added

### Version 0.4.0
- Initial stable release
- Core origin manipulation features
- Basic axis reorientation functionality
- Mesh alignment (experimental)

## Support & Contributing

### Report Issues
Found a bug or have a feature request? Please open an issue on GitHub:
[https://github.com/dmcoy/origin-tools/issues](https://github.com/dmcoy/origin-tools/issues)

### Contributing
Contributions welcome! Feel free to submit pull requests for:
- Bug fixes
- New features (please discuss first in issues)
- Documentation improvements
- Code enhancements (following PEP8 style guidelines)

See the [GitHub repository](https://github.com/dmcoy/origin-tools) for more information.

## Credits

- Original mesh alignment algorithm adapted from [Auto-Align](https://github.com/cube-c/Auto-Align) (unlicensed reference material)
- Blender Foundation for the incredible open-source 3D creation suite

---

[GitHub Repository](https://github.com/dmcoy/origin-tools) | [Blender Extensions Platform](https://extensions.blender.org)