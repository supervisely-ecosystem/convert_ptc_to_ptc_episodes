<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/106374579/183427800-8d0cd4c1-0aef-4e9e-8d81-7c27b8d3a019.png"/>

# Convert point clouds project to episodes

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a>
</p>


[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/convert_ptc_to_ptc_episodes)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/convert_ptc_to_ptc_episodes)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/convert_ptc_to_ptc_episodes.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/convert_ptc_to_ptc_episodes.png)](https://supervise.ly)

</div>

# Overview

Convert point clouds project to [Point Cloud Episodes format](https://docs.supervise.ly/data-organization/00_ann_format_navi/07_supervisely_format_pointcloud_episode). All figures (3D bounding boxes) with the same `object_id` from different point clouds will be united to tracklets.

It is useful app If you have point clouds project and you want to apply 3D tracking tools and export project annotations with tracklets in convinient to use format.

Supervisely has specially designed annotation tool for point cloud episodes with support of photo context, here is the example:

<img src="https://github.com/supervisely-ecosystem/convert_ptc_to_ptc_episodes/releases/download/v0.0.1/episode-o.gif"/>

# How To Use
**Step 1**: Add app to your team from [Ecosystem](https://ecosystem.supervise.ly/apps/convert_ptc_to_ptc_episodes)

**Step 2**: Open context menu of point clouds project -> `Run App` -> `Convert point clouds project to episodes`. Click "RUN" in opened modal window.

<img src="https://user-images.githubusercontent.com/97401023/173357403-9aa96b83-7480-4264-bdd4-e4a1238993c4.png" width="600px"/>

**Step 3**: Result project will be available to see in `Tasks` list (image below) or from `Projects` in workspace of your source point clouds project

<img src="https://user-images.githubusercontent.com/97401023/173357522-72e2e6ec-5642-4f6d-bf80-1221ad8babe9.png">
