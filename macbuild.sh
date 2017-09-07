#!/bin/sh

./macbuild-PnWork.sh

#####
# Set this variable to exclude file resource forks from
# tar archives on macOS.
export COPYFILE_DISABLE=true

APPNAME="ClockworkVMs"
APPVERSION="0.9.4.1"
APPICON=""

PERL="/usr/bin/perl"
MV="/bin/mv"
RM="/bin/rm"
ECHO="/bin/echo"
CP="/bin/cp"
TAR="/usr/bin/tar"
PWD="/bin/pwd"
MKDIR="/bin/mkdir"
MKTEMP="/usr/bin/mktemp"
SUDO="/usr/bin/sudo"
MAKE="/usr/bin/make"
CS="/usr/bin/codesign"

PYUIC="/usr/local/bin/pyuic5"

PYINSTALLER_MAKESPEC="/usr/local/bin/pyi-makespec"
PYINSTALLER_BUILD="/usr/local/bin/pyinstaller"

###################################################
# Set these variables to make sure pyinstaller can
# find the tool libraries to build PyQt5 applications
export PYTHONPATH=/opt/tools/lib/Python/2.7/site-packages:/opt/tools/lib/Python/2.7/site-packages/PyQt5:/opt/tools/lib/Qt5.6.1/lib:/opt/tools/lib/Python/2.7/site-packages/sip:$PYTHONPATH
export DYLD_LIBRARY_PATH=/opt/tools/lib/Qt5.6.1/lib:/opt/tools/lib/Python/2.7/site-packages:/opt/tools/lib/Python/2.7/site-packages/PyQt5:/opt/tools/lib/Python/2.7/site-packages/sip:$DYLD_LIBRARY_PATH
export DYLD_FRAMEWORK_PATH=/opt/tools/lib/Qt5.6.1/lib:/opt/tools/lib/Python/2.7/site-packages:/opt/tools/lib/Python/2.7/site-packages/PyQt5:/opt/tools/lib/Python/2.7/site-packages/sip:$DYLD_FRAMEWORK_PATH
export LD_FRAMEWORK_PATH=/opt/tools/lib/Qt5.6.1/lib:/opt/tools/lib/Python/2.7/site-packages:/opt/tools/lib/Python/2.7/site-packages/PyQt5:/opt/tools/lib/Python/2.7/site-packages/sip:$LD_FRAMEWORK_PATH
export LD_LIBRARY_PATH=/opt/tools/lib/Qt5.6.1/lib:/opt/tools/lib/Python/2.7/site-packages:/opt/tools/lib/Python/2.7/site-packages/PyQt5:/opt/tools/lib/Python/2.7/site-packages/sip:$LD_LIBRARY_PATH

#####
# Change version string in Lanl_Fv2.py
${ECHO} "Changing version string in ${APPNAME}..."
SEDSTRING="s/\d+\.\d+\.\d+\.\d+/$APPVERSION/"
${PERL} -pe ${SEDSTRING} ./${APPNAME}.py > ./${APPNAME}.py.new
$RM ./${APPNAME}.py
$MV ./${APPNAME}.py.new ./${APPNAME}.py

###################################################
# to compile the UI:
${ECHO} "Compiling Qt ui files to a python files..."
${PYUIC} ui/ConfigureRepos.ui > ui/ConfigureRepos_ui.py
${PYUIC} ui/admin_credentials.ui > ui/admin_credentials_ui.py
${PYUIC} ui/PrepareIso.ui > ui/PrepareIso_ui.py
${PYUIC} ui/VirtualMachineBuilder.ui > ui/VirtualMachineBuilder_ui.py
${PYUIC} ui/VMSettings_ui.ui > ui/VirtualMachineSettings_ui.py

###################################################
# to compile a pyinstaller spec file for app creation:
${ECHO} "Creating a pyinstaller spec file for the project..."
#${PYINSTALLER_MAKESPEC} -w ${APPNAME}.py --noupx 
${PYINSTALLER_MAKESPEC}  -D -d --noupx -i ${APPICON} -w -p /opt/tools/lib/Python/2.7/site-packages/PyQt5:/opt/tools/Qt5.6.1/lib:/opt/tools/lib/Python/2.7/site-packages:/opt/tools/lib/Python/2.7/site-packages/sip/PyQt5:/opt/tools/bin:/usr/lib --osx-bundle-identifier gov.lanl.${APPNAME} ./${APPNAME}.py &> pyinstaller_makespec.log

###################################################
#to build:

# SET THE APP VERSION IN THE SPEC FILE

${ECHO} "Building the app..."
${PYINSTALLER_BUILD} -y --clean ${APPNAME}.spec --log-level=DEBUG &> pyinstaller_build.log 

######
# edit the .app's Info.plist & change the default value for CFBundleIconFile to your icon file (must be an icns file)
${ECHO} "Replacing string in Info.plist for the new icon..."
${PERL} -pe 's/icon-windowed/oxLock/' ./dist/${APPNAME}.app/Contents/Info.plist > dist/${APPNAME}.app/Contents/Info.plist.new
${RM} ./dist/${APPNAME}.app/Contents/Info.plist
${MV} ./dist/${APPNAME}.app/Contents/Info.plist.new ./dist/${APPNAME}.app/Contents/Info.plist

${ECHO} "Changing .app version string..."
SEDSTRING="s/\d+\.\d+\.\d+\.\d+/$APPVERSION/"
${PERL} -pe ${SEDSTRING} ./dist/${APPNAME}.app/Contents/Info.plist > dist/${APPNAME}.app/Contents/Info.plist.new
${RM} ./dist/${APPNAME}.app/Contents/Info.plist
${MV} ./dist/${APPNAME}.app/Contents/Info.plist.new ./dist/${APPNAME}.app/Contents/Info.plist


#####
# Make sure the "tarfiles" directory exists, so we can archive
# tarfiles of the name $APPNAME-$APPVERSION.app.tar.gz there
if [ ! -e "./dist/${APPNAME}.app/Contents/Resources/lib" ]; then
    mkdir "./dist/${APPNAME}.app/Contents/Resources/lib"
else
    if [ ! -d "./dist/${APPNAME}.app/Contents/Resources/lib" ]; then
        TMPFILE=`${MKTEMP} -d ../lib.XXXXXXXXXXXX`
        mv ./dist/${APPNAME}.app/Contents/Resources/lib ${TMPFILE}
        mkdir ./dist/${APPNAME}.app/Contents/Resources/lib
    fi
fi

#####
# Copy files to the resources directory
${CP} ${APPICON} ./dist/${APPNAME}.app/Contents/Resources

/bin/sync
/bin/sync

#####
# Sign the app before packaging:
UNLOCK_KEYCHAIN_OUTPUT=`/usr/bin/security unlock-keychain ${HOME}/Library/Keychains/login.keychain-db`
/bin/echo ${UNLOCK_KEYCHAIN_OUTPUT}
SIGNING_OUTPUT=`/usr/bin/codesign -vvvv --deep -f -s 'Mac Developer:' --keychain="${HOME}/Library/Keychains/login.keychain-db" ./dist/PNpass.app`
/bin/echo ${SIGNING_OUTPUT}

#####
# Make sure the "tarfiles" directory exists, so we can archive
# tarfiles of the name $APPNAME-$APPVERSION.app.tar.gz there
if [ ! -e "../tarfiles" ]; then
    mkdir "../tarfiles"
else
    if [ ! -d "../tarfiles" ]; then
        TMPFILE=`${MKTEMP} -d ../tarfiles.XXXXXXXXXXXX`
        mv ../tarfiles ${TMPFILE}
        mkdir ../tarfiles
    fi
fi

#####
# tar up the app and put it in the tarfiles directory
#${ECHO} "Tarring up the app & putting the tarfile in the ../build directory"
#cd dist; ${PWD}; ${TAR} czvf ../../tarfiles/${APPNAME}-${APPVERSION}.app.tar.gz ${APPNAME}.app; cd ..

###################################################
# to create the package
${ECHO} "Putting new version into Makefile..."
SEDLINE="s/PACKAGE_VERSION=\d+\.\d+\.\d+\.\d+/PACKAGE_VERSION=${APPVERSION}/"
${PERL} -pe ${SEDLINE} Makefile > Makefile.new
${RM} Makefile
${MV} Makefile.new Makefile

if [ ! -e "../dmgs" ]; then
    mkdir "../dmgs"
else
    if [ ! -d "../dmgs" ]; then
        TMPFILE=`${MKTEMP} -d ../dmgs.XXXXXXXXXXXX`
        mv ../dmgs ${TMPFILE}
        mkdir ../dmgs
    fi
fi

${ECHO} "Creating a .pkg filefor installation purposes..."
${SUDO} ${MAKE} pkg
${ECHO} "Moving the pkg to the ../dmgs directory."
${MV} ${APPNAME}-${APPVERSION}.pkg ../dmgs


