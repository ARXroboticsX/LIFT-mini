#!/bin/bash
rm -rf build
cmake -B build && cmake --build build && cmake --install build
