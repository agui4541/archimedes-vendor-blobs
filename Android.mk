# Copyright (C) 2026 Archimedes contributors
# SPDX-License-Identifier: Apache-2.0

LOCAL_PATH := $(call my-dir)

ifeq ($(TARGET_DEVICE),archimedes)
include $(LOCAL_PATH)/archimedes-vendor.mk
endif
