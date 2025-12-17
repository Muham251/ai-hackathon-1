---
id: urdf-essentials
title: "URDF Basics for Humanoid Models"
sidebar_label: URDF for Humanoids
---

The **Unified Robot Description Format (URDF)** is an XML format used in ROS to describe all the physical elements of a robot model. For a humanoid, the URDF file is its digital blueprint. It defines the robot's body parts, how they are connected, and their physical properties.

A URDF file describes the robot as a tree of **links** connected by **joints**.

- **`<link>`**: A physical part of the robot (e.g., a forearm, a foot, a torso).
- **`<joint>`**: The connection between two links. It defines how one link moves relative to another (e.g., rotating like an elbow, sliding, or being fixed).

### Key URDF Tags

#### The `<robot>` Tag
Every URDF file must start and end with the `<robot>` tag. It's the root element, and you give your robot a name here.
```xml
<robot name="simple_humanoid">
  ... all your links and joints go here ...
</robot>
```

#### The `<link>` Tag
Each link has a name and can contain three important sub-tags:
- **`<visual>`**: Defines the appearance of the link (shape, size, color, texture). This is what you see in simulation tools like RViz.
- **`<collision>`**: Defines the collision geometry of the link. This is what the physics engine uses to calculate collisions with other objects. It's often a simpler shape than the visual one for performance reasons.
- **`<inertial>`**: Defines the dynamic properties of the link: its mass, center of mass, and inertia matrix. This is crucial for realistic physics simulation.

```xml
<link name="torso">
  <visual>
    <geometry>
      <box size="0.2 0.3 0.5"/>
    </geometry>
    <material name="grey">
      <color rgba="0.5 0.5 0.5 1"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <box size="0.2 0.3 0.5"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="10"/>
    <inertia ixx="0.4" ixy="0.0" ixz="0.0" iyy="0.4" iyz="0.0" izz="0.2"/>
  </inertial>
</link>
```

#### The `<joint>` Tag
Each joint connects two links, called the **parent** and the **child**. It also defines the motion allowed between them.

- **`name`**: The name of the joint (e.g., "left_shoulder_joint").
- **`type`**: The type of motion. Common types are:
  - `revolute`: Rotates around an axis (like an elbow). Requires `<limit>` tags for upper and lower angles.
  - `continuous`: Rotates around an axis with no angle limits.
  - `prismatic`: Slides along an axis (like a piston).
  - `fixed`: No motion is allowed between the two links.
- **`<parent link="..." />`**: The name of the parent link.
- **`<child link="..." />`**: The name of the child link.
- **`<origin xyz="..." rpy="..." />`**: The transform (position and orientation) from the parent link's origin to the joint's origin.
- **`<axis xyz="..." />`**: The axis of rotation or translation for `revolute` and `prismatic` joints.

```xml
<joint name="neck_joint" type="revolute">
  <parent link="torso"/>
  <child link="head"/>
  <origin xyz="0 0 0.25" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-0.5" upper="0.5" effort="10" velocity="1.0"/>
</joint>
```

### Simple Humanoid URDF Example

This example describes a very simple humanoid robot. It has a torso, a head, and a single arm with a shoulder and elbow joint. This demonstrates the parent-child tree structure. The "torso" is the root link of our tree.

```xml
<!-- simple_humanoid.urdf -->
<robot name="simple_humanoid">

  <!-- A. Materials (for color) -->
  <material name="blue">
    <color rgba="0.0 0.0 0.8 1.0"/>
  </material>
  <material name="white">
    <color rgba="1.0 1.0 1.0 1.0"/>
  </material>

  <!-- B. Base Link (Torso) -->
  <link name="torso">
    <visual>
      <geometry><box size="0.2 0.3 0.5"/></geometry>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <material name="blue"/>
    </visual>
    <collision><geometry><box size="0.2 0.3 0.5"/></geometry></collision>
    <inertial>
        <mass value="10"/>
        <inertia ixx="1.0" ixy="0" ixz="0" iyy="1.0" iyz="0" izz="1.0"/>
    </inertial>
  </link>

  <!-- C. Head Link -->
  <link name="head">
    <visual>
      <geometry><sphere radius="0.1"/></geometry>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <material name="white"/>
    </visual>
    <collision><geometry><sphere radius="0.1"/></geometry></collision>
    <inertial>
        <mass value="1"/>
        <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- D. Neck Joint (Connects Torso to Head) -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.30" rpy="0 0 0"/> <!-- Position of head relative to torso -->
    <axis xyz="0 0 1"/>
    <limit lower="-0.7" upper="0.7" effort="5" velocity="0.5"/>
  </joint>

  <!-- E. Right Arm -->
  <link name="right_upper_arm">
    <visual>
        <geometry><cylinder length="0.3" radius="0.05"/></geometry>
        <origin xyz="0 0 -0.15" rpy="0 0 0"/>
        <material name="white"/>
    </visual>
    <collision><geometry><cylinder length="0.3" radius="0.05"/></geometry></collision>
    <inertial>
        <mass value="2"/>
        <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- F. Right Shoulder Joint -->
  <joint name="right_shoulder_joint" type="revolute">
      <parent link="torso"/>
      <child link="right_upper_arm"/>
      <origin xyz="0 -0.20 0.15" rpy="1.5707 0 0"/> <!-- Position of arm relative to torso -->
      <axis xyz="0 0 1"/>
      <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
  </joint>

</robot>
```

#### How to Use This URDF
1.  Save the code above as `simple_humanoid.urdf`.
2.  You can check its validity using the `check_urdf` command: `check_urdf simple_humanoid.urdf`.
3.  To visualize it, you can use ROS tools like RViz. This typically requires a small launch file to publish the robot's state, which is a topic for a later module.

This simple example provides the foundation. A full humanoid model would extend this tree with more links and joints for the legs, a more complex arm, and hands.