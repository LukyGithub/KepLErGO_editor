# This is a track editor for the [main code](https://github.com/LukyGithub/RobotMain) for [FLL 2021](https://firstlegoleague.org/season) <img src="https://user-images.githubusercontent.com/70636940/140644407-2680a70c-2267-4700-b7f1-72df1e2519ed.png" alt="Fll" width="50"/>
- This is in unfinished state (missing features)
- Press left mouse button to add point on screen or press ```A``` to manually add a point by typing numbers ```(format: x, y)``` and pressing enter
- Press right mouse button while hovering over a point to open a text editor relative to that point
- press ```Z``` to undo the last point added
  - The text editor is used to write code which will execute after the robot arrives to the point that you are editing its code
    - In the editor press ```Enter/Return``` to make a new line
    - Backspace to delete previous character
    - Any letter to add to the text
- press ```L``` to see line lenghts

Done:
- [x] Drawing the background
- [x] Adding/Removing points
- [x] Opening/Closing menus and storing their text
- [x] Text editor
- [x] Manual adding points
- [x] Exporting into a .txt file for RobotMain to read
- [x] Converting pixelspace into map relative space
- [x] Show how long travel lines take
- [x] Make an icon for the app
- [x] Load map info
- [x] Make layers (to make it more pleasing to look at)

Todo:

- [ ] Zooming in and out on the map

Optional:

- [ ] Make shortcuts with CTRL
- [ ] Camera movement whilst zoomed in
- [ ] Make a better map
- [ ] Add a robot picture under your cursor (for more percise Trial-and-error)