# Porting.md
# Progress Tracking

## Completed 
- [x] Updated gi.require_version calls to 4.0 in Python files
- [x] Updated import statements
- [x] Updated build system GIR includes (Gtk-4.0, Gdk-4.0)
- [x] Fixed GdkEvent opaque struct access in sugar-event-controller.c
- [x] Fixed GTK 4 event handling in all event controllers
- [x] Migrated from GdkPoint to custom SugarPoint structure

## In Progress 
- [ ] Find and update remaining 3.0 version references
- [ ] Fix eggaccelerator errors

## TODO 
- [ ] Replace GtkToolbar with GtkBox
- [ ] Migrate GtkEventBox to GtkWidget + EventControllers  
- [ ] Update GtkContainer usage to new child management
- [ ] Convert draw() methods to snapshot()
- [ ] Update size request/allocation APIs
- [ ] Replace widget "event" signal with proper event controllers

## Breaking Changes  

- **GdkEvent Opaque Structure**: In GTK 4, GdkEvent structs are now opaque and immutable. Direct field access like `event->type` and `event->grab_broken.keyboard` is no longer allowed.
  - Solution: Use accessor functions like `gdk_event_get_event_type()` 
  - Reference: https://docs.gtk.org/gdk4/class.Event.html

- **GDK_GRAB_BROKEN Event Removed**: The GDK_GRAB_BROKEN event type and related grab broken handling has been removed/changed in GTK 4.
  - Solution: Removed grab broken handling entirely as GTK 4 uses automatic grab management
  - Reference: https://docs.gtk.org/gtk4/input-handling.html

- **GdkPoint Removed**: The GdkPoint structure was removed in GTK 4.
  - Solution: Created custom SugarPoint structure for internal use
  - Reference: https://docs.gtk.org/gtk4/migrating-3to4.html

- **Event Coordinate Access**: Direct access to event coordinates changed in GTK 4.
  - Old: `event->touch.x`, `event->touch.y`
  - New: `gdk_event_get_position(event, &x, &y)`
  - Reference: https://docs.gtk.org/gdk4/method.Event.get_position.html

- **Widget "event" Signal**: The generic widget "event" signal is deprecated in favor of specific event controllers.
  - Current Status: Still using for compatibility, needs migration to proper event controllers
  - Reference: https://docs.gtk.org/gtk4/input-handling.html

## Build Status 
- Last successful build: Pending - working on build system updates
- Current blockers: Need to update configure.ac and remaining GTK 3.0 references

# Changes Tracking and Implementation Details

## Event System Migration

### Fixed Issues:
1. **sugar-event-controller.c**: Removed direct GdkEvent field access and grab broken handling
   - Removed: `event->type == GDK_GRAB_BROKEN && !event->grab_broken.keyboard`
   - Added comment about GTK 4's automatic grab management

2. **sugar-long-press-controller.c**: Migrated to GTK 4 event API
   - Fixed: `event->type` → `gdk_event_get_event_type()`
   - Fixed: `event->touch.x/y` → `gdk_event_get_position()`
   - Fixed: `gdk_threads_add_timeout()` → `g_timeout_add()`

3. **sugar-swipe-controller.c**: Migrated to GTK 4 event API
   - Fixed: `gdk_event_get_coords()` → `gdk_event_get_position()`
   - Fixed: `event->type` → `gdk_event_get_event_type()`

4. **sugar-touch-controller.c**: Migrated to GTK 4 event API and data structures
   - Fixed: `GdkPoint` → `SugarPoint` (custom structure, made a new struct)
   - Fixed: `event->type` → `gdk_event_get_event_type()`
   - Fixed: `event->touch.x/y` → `gdk_event_get_position()`

### References:
- https://docs.gtk.org/gdk4/class.Event.html
- https://docs.gtk.org/gtk4/input-handling.html
- https://docs.gtk.org/gdk4/method.Event.get_position.html
- https://docs.gtk.org/gdk4/method.Event.get_event_type.html
