#!/bin/bash

# Function to detect RHEL-based OS version using PLATFORM_ID and set the appropriate URL
detect_os() {
    PLATFORM_ID=$(grep "^PLATFORM_ID=" /etc/os-release | cut -d ':' -f2)

    if [ "$PLATFORM_ID" == "el8" ]; then
        OS_VERSION="el8"
        PACKAGE_URL="https://parts.centminmod.com/centminmodparts/screen/el8/screen-5.0.0-1.el8.x86_64.rpm"
    elif [ "$PLATFORM_ID" == "el9" ]; then
        OS_VERSION="el9"
        PACKAGE_URL="https://parts.centminmod.com/centminmodparts/screen/el9/screen-5.0.0-1.el9.x86_64.rpm"
    else
        echo "Unsupported OS version. This script only supports RHEL-based OS with platform ID 'el8' or 'el9'."
        exit 1
    fi
}

# Function to download and install the appropriate package
install_screen() {
    echo "Detected RHEL-based OS $OS_VERSION"
    echo "Downloading screen package from $PACKAGE_URL"
    wget -q $PACKAGE_URL -P /tmp

    if [ $? -ne 0 ]; then
        echo "Failed to download the screen package. Please check the URL and try again."
        exit 1
    fi

    PACKAGE_FILE=$(basename $PACKAGE_URL)

    echo "Installing screen package..."
    yum -y install /tmp/$PACKAGE_FILE

    if [ $? -eq 0 ]; then
        echo "Screen successfully installed."
        # Cleanup
        rm -f /tmp/$PACKAGE_FILE
    else
        echo "Failed to install the screen package. Please check the installation logs."
        exit 1
    fi
}

# Main script execution
detect_os
install_screen
