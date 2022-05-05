# Telus IoT Starter Kit Walkthrough: Part 2

This is part 2 of a 3-part tutorial that will help get you started with the TELUS LTE-M IoT Starter Kit:
* **[Part 1](https://github.com/briantan050/Telus-IoT-Starter-Kit-Walkthrough-Part-1/)** will give you some background on the kit and walk you through the process of getting the kit configured to send data to your own Microsoft Azure instance.
* **[Part 2](https://github.com/briantan050/Telus-IoT-Starter-Kit-Walkthrough-Part-2/)** will walk you through using the IoT data in a logic app with the Copernicus open access hub API. 
* **[Part 3](https://github.com/briantan050/Telus-IoT-Starter-Kit-Walkthrough-Part-3/)** will walk you through displaying the IoT data in a Power BI dashboard.

### Logic app functions
Now that you have sensor data being sent to your Azure IoT Hub, it would be useful to perform automated actions on it when certain criteria is met. Logic apps allow you to perform automated workflows and functions with your data and apps. This tutorial will walk you through the process of creating a Logic App with your IoT data. 

The goal of this app will be to automatically download recent satellite imagery from given GPS coordinates from [Copernicus Open Access Hub](https://scihub.copernicus.eu/) when certain criteria is met. The Logic App will decode the IoT data, filter for a certain condition, send GPS coordinates to the connected Copernicus API, and retrieve the URL to download the satellite mapsheet. 

The list of steps is as follows:
* Configuring Azure
* Configuring Power BI

### Requirements
1. [Telus IOT Starter Kit](https://www.avnet.com/shop/us/products/avnet-engineering-services/aes-bg96-iot-sk2-g-3074457345636408150?INTCMP=tbs_low-power-wide-area_button_buy-your-kit)
2. [Microsoft Azure Account](https://azure.microsoft.com/en-ca/)
3. [Copernicus Open Access Hub Account](https://scihub.copernicus.eu/dhus/#/self-registration) (free to register)
4. Basic knowledge of Python is an asset

# Configuring Azure
### Create a Logic App






## Done
Your board is now sending sensor data to Azure IoT Hub on a regular basis. In this tutorial, you have completed the following:
* Created an Azure IoT Hub
* Registered your IoT device on the Azure IoT Hub
* Compiled the Azure IoT MBed client and loaded it onto your IoT device
* Successfully sent data from your IoT device to Azure IoT Hub
* Monitored the contents of the incoming JSON payloads with the Azure CLI tool 

## Next steps
If you are interested in displaying the IoT data in a Power BI dashboard, continue on to **[Part 3](https://github.com/briantan050/Telus-IoT-Starter-Kit-Walkthrough-Part-3/)**.

## Credits:
* GarettB's tutorial: [TELUS IOT Getting Started](https://github.com/garettB/TELUS_IoT_Getting_Started)
* Microsoft Azure's tutorial: [Visualize real-time sensor data from Azure IoT Hub using Power BI](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-live-data-visualization-in-power-bi)
* Dinusha Kumarasiri's tutorial: [End to end IoT Solution with Azure IoT Hub, Event Grid and Logic Apps](https://youtu.be/Wb_QT0qHGOo)
* Reza Vahidnia and F. John Dian's book: [Cellular Internet of Things for Practitioners](https://pressbooks.bccampus.ca/cellulariot/)
