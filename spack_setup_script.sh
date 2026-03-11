#!/bin/bash

usage() {
    cat << EOF
    Usage: $0 [-HUR] [-S system] [-E profile file]
     -H Display this and quit.
     -U Do a "git pull" before installing.
     -R Install custom CUP-ECS and COMPASS Spack package repositories
        Note: It is also a good idea to check in all code in "spack develop" before running this command!
     -S [system] Provide this value if you wish to install for a value different than what is in "\$CLUSTER".
        Note: This value is required if \$CLUSTER is not set. This is destructive and will override any local
        adjustments to your system packages and/or repo package.yaml files! 
     -E [file] If you wish to have this script to setup Spack such that is automatically sourced upon log in,
        set this value. TODO -- note about other vars
EOF
}

while getopts ":UR:S:E:" opt; do
    case $opt in
        U)
            GET_UPDATE=1
            ;;
        R)
            SPACK_REPO_SETUP=1
            WANT_SPACK=1
            ;;
        S)
            CLUSTER="$OPTARG"
            ;;
        E)
            PROFILE_FILE="$OPTARG"
            WANT_SPACK=1
            ;;
        *)
            usage
            exit
            ;;
    esac
done

# Check if "CLUSTER" is available
if [ -z $CLUSTER ]; then
    echo "No system specified -- exiting". 
    exit 1
fi
# Check if we know about cluster
if [ ! -d $(pwd)/system_externals/$CLUSTER ]; then
    echo "No packages for system -- exiting."
    exit 1
fi
# Now install the file.
INSTALL_FILE=$(pwd)/system_externals/$CLUSTER/packages.yaml
INSTALL_LOCATION=$HOME/.spack/$CLUSTER/
# Check if install location exists
if [ ! -d $INSTALL_LOCATION ]; then
    echo "Making folder for $CLUSTER external packages"
    mkdir -p $INSTALL_LOCATION
fi

# Check if file is present.
if [ -f $INSTALL_LOCATION/packages.yaml ]; then
    hash1=$(sha1sum "$INSTALL_FILE" | cut -d' ' -f1)
    hash2=$(sha1sum "$INSTALL_LOCATION/packages.yaml" | cut -d' ' -f1)
    # If present, check if it is same version as what is in repository
    if [ ! "$hash1" == "$hash2" ]; then
        echo "Current packages file does not match repo, will replace"
        NEED_NEW_FILE=1
    fi
else
    NEED_NEW_FILE=1
fi

# If determined that the package file for the cluster is needed, install it
if [ -v $NEED_NEW_FILE ]; then
    echo "Installing $INSTALL_FILE to $INSTALL_LOCATION"
    cp $INSTALL_FILE $INSTALL_LOCATION
fi

# Update git repository for latest files
# Technically, this script may be replaced by the git pull, so any changes
# in this script will not be carried out until the next time the script runs.
if [ -v $GET_UPDATE ]; then
    echo "Pulling latest code"
    git pull
fi

# If no actions need a working Spack, we can stop here.
if [ ! -v $WANT_SPACK ]; then
    exit 0
fi

# Before working on anything related to Spack, check for Spack install
if ! which spack; then
    echo "No spack installed -- stopping"
    exit 1
fi
SPACK_EXE=$(which spack)

# If the user wants us to setup the Spack package repositories for them
if [ -v $SPACK_REPO_SETUP ]; then
    echo "Removing old spack repositories"
    spack repo remove cupecs
    spack repo remove compass
    spack repo add $(pwd)/spack_pkgs/spack_repo/cupecs
    spack repo add $(pwd)/spack_pkgs/spack_repo/compass
fi

# If the user wants to setup Spack to be sourced upon login:
if [ -v $PROFILE_FILE ]; then
    if [ ! $HOME/$PROFILE_FILE ]; then
        echo "$HOME/$PROFILE_FILE does not exist -- stopping"
        exit 1 
    fi

    STRING_TO_ADD="export SPACK_USER_CONFIG_PATH=\$HOME/.spack/\$CLUSTER"
    if ! grep -Fxq "$STRING_TO_ADD" "$HOME/$PROFILE_FILE"; then
        echo "Adding \"$STRING_TO_ADD\" to \"$HOME/$PROFILE_FILE\"."
        printf '%s\n' "$STRING_TO_ADD" >> "$HOME/$PROFILE_FILE"
    else
        echo "Spack already 
    fi
fi