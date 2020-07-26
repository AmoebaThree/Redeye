# Redeye

Obstacle detector

## Message Spec

Format: \<channel> "message"

### Inputs

* \<redeye.line> *
  * Triggers a request for status of the line sensors
  * Only if this Redeye is running in Line mode
* \<redeye.obstacle> *
  * Triggers a request for status of the obstacle sensors
  * Only if this Redeye is running in obstacle mode

### Outputs

* \<redeye.line.left> "redeye.line.left.on"
  * Left line sensor on, sensor has been triggered
  * Only if the this Redeye is running in Line mode
  * Triggered automatically, or in response to a line input query
* \<redeye.line.left> "redeye.line.left.off"
  * Left line sensor off, sensor has been un-triggered
  * Only if the this Redeye is running in Line mode
  * Triggered automatically, or in response to a line input query
* \<redeye.line.right> "redeye.line.right.on"
  * Right line sensor on, sensor has been triggered
  * Only if the this Redeye is running in Line mode
  * Triggered automatically, or in response to a line input query
* \<redeye.line.right> "redeye.line.right.off"
  * Right line sensor off, sensor has been un-triggered 
  * Only if the this Redeye is running in Line mode
  * Triggered automatically, or in response to a line input query
* \<redeye.obstacle.left> "redeye.obstacle.left.on"
  * Left obstacle sensor on, sensor has been triggered
  * Only if the this Redeye is running in obstacle mode
  * Triggered automatically, or in response to a obstacle input query
* \<redeye.obstacle.left> "redeye.obstacle.left.off"
  * Left obstacle sensor off, sensor has been un-triggered
  * Only if the this Redeye is running in obstacle mode
  * Triggered automatically, or in response to a obstacle input query
* \<redeye.obstacle.right> "redeye.obstacle.right.on"
  * Right obstacle sensor on, sensor has been triggered
  * Only if the this Redeye is running in obstacle mode
  * Triggered automatically, or in response to a obstacle input query
* \<redeye.obstacle.right> "redeye.obstacle.right.off"
  * Right obstacle sensor off, sensor has been un-triggered 
  * Only if the this Redeye is running in obstacle mode
  * Triggered automatically, or in response to a obstacle input query