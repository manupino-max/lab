# M3 next gate — artifact metadata completeness — 2026-08-14

## Purpose
After closing byte-level CI artifact parity, verify that evidence records all provenance identifiers needed for promotion.

## Required fields
- commit SHA
- workflow run ID
- job ID
- artifact ID
- artifact archive SHA-256
- extracted payload SHA-256
- configuration identifier/hash
- row count
- interpretation class

## Current known values
- commit: `7c842feaf63b4d8175537c8906328a046b923998`
- run: `31793329664`
- jobs: `94744880260`, `94744880288`
- artifacts: `9216353407`, `9216353258`
- archive SHA-256: `ffacdaff7d8530e8e04c106f88e295f215d74c314686b84f72fd9c21152170bd`
- payload SHA-256: `343ec6d6410ddd2b27a5845c0b4054435b15ab63dff20f6d90b820e2d4fcb49d`
- rows: `64`
- interpretation: infrastructure reproducibility only

## Status
OPEN — this is the next concrete M3 control; it does not block independent work and does not alter E8/E12 scientific protocol.
