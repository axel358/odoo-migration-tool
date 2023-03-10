pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'odoomigrationtool')
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'window.blp',
    'new-session-dialog.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('odoomigrationtool',
  'odoomigrationtool.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'odoomigrationtool.in',
  output: 'odoomigrationtool',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

odoomigrationtool_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'session.py',
]

install_data(odoomigrationtool_sources, install_dir: moduledir)
