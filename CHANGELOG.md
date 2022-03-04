# Changelog

## [0.1.3]
### Fixed
- Disable unused Qt translation for credits group title
- Initialize player with values from configuration
- Check if 'icy-sr' is in headers before parsing

### Added
- Add Bulgarian translation in the README
- Add I18n support
- Add Bulgarian translation
- Allow selecting output device from GUI

### Changed
- Clean up installation instructions in the README
- Enable word wrapping on settings labels
- Raise exception when device is missing in `check_output_device_params`
- Update dependencies
  - platformdirs 2.4.1 -> 2.5.1
  - pyqtdarktheme 1.0.3 -> 1.1.0
  - PySide6 6.2.2 -> 6.2.3

## [0.1.2]
### Fixed
- Compiled Qt modules missing in standard distribution and wheels

## [0.1.1]
### Fixed
- Add missing 'gui' extra install option
- Add missing internal modules to setup.cfg

## [0.1.0]
Initial release
