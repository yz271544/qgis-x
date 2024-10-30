### /usr/lib/x86_64-linux-gnu/qt5
export PATH="$OSGEO4W_ROOT/apps/qt5/bin:$PATH"
### /usr/lib/x86_64-linux-gnu/qt5/plugins
export QT_PLUGIN_PATH="$OSGEO4W_ROOT/apps/Qt5/plugins"
export O4W_QT_PREFIX="${OSGEO4W_ROOT//\\//}/apps/Qt5"
export O4W_QT_BINARIES="${OSGEO4W_ROOT//\\//}/apps/Qt5/bin"
export O4W_QT_PLUGINS="${OSGEO4W_ROOT//\\//}/apps/Qt5/plugins"
export O4W_QT_LIBRARIES="${OSGEO4W_ROOT//\\//}/apps/Qt5/lib"
export O4W_QT_TRANSLATIONS="${OSGEO4W_ROOT//\\//}/apps/Qt5/translations"
export O4W_QT_HEADERS="${OSGEO4W_ROOT//\\//}/apps/Qt5/include"
export O4W_QT_DOC="${OSGEO4W_ROOT//\\//}/apps/Qt5/doc"

#etl@etl-VMware20-1:/usr/lib/x86_64-linux-gnu/qt5$ cat qt.conf
#[Paths]
#Prefix=/usr
#ArchData=lib/x86_64-linux-gnu/qt5
#Binaries=lib/qt5/bin
#Data=share/qt5
#Documentation=share/qt5/doc
#Examples=lib/x86_64-linux-gnu/qt5/examples
#Headers=include/x86_64-linux-gnu/qt5
#HostBinaries=lib/qt5/bin
#HostData=lib/x86_64-linux-gnu/qt5
#HostLibraries=lib/x86_64-linux-gnu
#Imports=lib/x86_64-linux-gnu/qt5/imports
#Libraries=lib/x86_64-linux-gnu
#LibraryExecutables=lib/x86_64-linux-gnu/qt5/libexec
#Plugins=lib/x86_64-linux-gnu/qt5/plugins
#Qml2Imports=lib/x86_64-linux-gnu/qt5/qml
#Settings=/etc/xdg
#Translations=share/qt5/translations


#ls /usr/share/qt5/
#doc/          phrasebooks/  resources/    translations/
