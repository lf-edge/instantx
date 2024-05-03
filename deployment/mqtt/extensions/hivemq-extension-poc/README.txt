:hivemq-link: http://www.hivemq.com
:hivemq-extension-docs-link: http://www.hivemq.com/docs/extensions/latest/
:hivemq-extension-docs-archetype-link: http://www.hivemq.com/docs/extensions/latest/#maven-archetype-chapter
:hivemq-blog-tools: http://www.hivemq.com/mqtt-toolbox
:maven-documentation-profile-link: http://maven.apache.org/guides/introduction/introduction-to-profiles.html
:hivemq-support: http://www.hivemq.com/support/
:hivemq-testcontainer: https://github.com/hivemq/hivemq-testcontainer
:hivemq-mqtt-client: https://github.com/hivemq/hivemq-mqtt-client

== HiveMQ 4 Poc Extension

*Type*: Metrics Extension

*Version*: 1.0.1
*Generator Versions*: 4.6.3 (archetype and SDKExtension)

*License*: Apache License Version 2.0

=== Purpose

This extension recreates the same behavior as the existing HiveMQ Metrics Extension
provided by HiveMQ professional services team. It serves to demonstrate that the same
behavior can be implemented using the public extension archetypes.

There is {hivemq-extension-docs-archetype-link}[a Maven Archetype available]
to generate a basic extension from the IDE.

We strongly recommend to read the {hivemq-extension-docs-link}[HiveMQ Extension Documentation]
to grasp the core concepts of HiveMQ extension development.

=== Installation

. Clone this repository into a Java 11 maven project.
. Run `mvn package` goal from Maven to build the extension.
. Move the file: "target/hivemq-extension-poc-1.0.1-distribution.zip" to the directory: "HIVEMQ_HOME/extensions"
. Unzip the file.
. Start HiveMQ.

=== Need help?

If you encounter any problems, we are happy to help. The best place to get in contact is our {hivemq-support}[support].
