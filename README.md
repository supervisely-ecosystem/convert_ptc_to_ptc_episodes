<div align="center" markdown>
<img src=""/>

# Convert point clouds project to episodes

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a>
</p>


[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/export-to-supervisely-format)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/export-to-supervisely-format)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/convert_ptc_to_ptc_episodes&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/convert_ptc_to_ptc_episodes&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/convert_ptc_to_ptc_episodes&counter=runs&label=runs)](https://supervise.ly)

</div>

# Overview

Convert point clouds project to [Point Cloud Episodes format](https://docs.supervise.ly/data-organization/00_ann_format_navi/07_supervisely_format_pointcloud_episode). All figures (3D bounding boxes) with the same `object_id` from different point clouds will be united to tracklets.

It is useful app If you have point clouds project and you want to apply 3D tracking tools and export project annotations with tracklets in convinient to use format.

# How To Use
**Step 1**: Add app to your team from [Ecosystem](https://ecosystem.supervise.ly/apps/convert_ptc_to_ptc_episodes) if it is not there

**Step 2**: Open context menu of point clouds project -> `Run App` -> `Convert point clouds project to episodes` 

<img src="" width="600px"/>

**Step 3 (optional)**: Define application launch settings in modal window

<img src="" width="600px">

**Step 4**: Result project will be available to see in `Tasks` list (image below) or from `Projects` in workspace of your source point clouds project

<img src="">
