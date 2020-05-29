#!/bin/bash
export DOTNET_ROOT=/snap/dotnet-sdk/current
export MSBuildSDKsPath=$DOTNET_ROOT/sdk/$(${DOTNET_ROOT}/dotnet --version)/Sdks
export PATH="${PATH}:${DOTNET_ROOT}"

export PATH="$PATH:$HOME/.dotnet/tools"
