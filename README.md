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
1. In the Azure portal, select **Create a resource**. 
![image](https://user-images.githubusercontent.com/53897474/158875955-2c17f1c8-20d5-4388-86e2-4da128a7832f.png)

2. Type **Logic app** in the search box and select it from the drop-down list. 
3. On the Logic app overview page, select **Create**
4. Enter the following information for the Logic app:  

* **Subscription**: Select your existing subscription or create a new one.
* **Resource Group**: Select your existing Resource Group or create a new one.
* **Logic App name**: Choose a name for your Logic App. This can be anything.
* **Region**: Use the same location as your resource group.
* **Enable log analytics**: Select **No**
* **Plan type**: Select **Consumption**

![image](https://user-images.githubusercontent.com/53897474/167044055-bd428dd2-c926-423c-8878-46029cd6ddb3.png)

5. Select **Review + Create**, and then **Create**.

### Configure the Logic App
1. Open the Logic App.
2. Scroll down and select **Blank Logic App**
3. On the top toolbar, select **Code view**.
4. Replace the existing code with the code from **logic_app_code.txt**. 
5. At the top toolbar, select **Save**.
6. At the top toolbar, select **Designer** to open the design view.
7. Select the first block, the Trigger, to open it.
8. Copy the **HTTP POST URL**. We will need it for the next step.  
![image](https://user-images.githubusercontent.com/53897474/167047536-f6fed635-8d10-4ec4-ae65-896e5c93d189.png)  
9. Navigate back to your Azure Portal home screen.

### Create a subscription event
1. In the Azure portal, open your IoT Hub.
2. On the left toolbar, select **Events**.
3. At the top toolbar, select **Event Subscription**.
4. Enter the following information for the Event Subscription:

* **Name**: Choose a name for your subscription. This can be anything.
* **Event Schema**: Event Grid Schema
* **Filter to Event Types**: Only select **Device Telemetry**
* **Endpoint Type**: Web Hook
* **Endpoint**: Paste the **HTTP POST URL** that you copied earlier, and select **Confirm Selection**. 
* Select **Create**.
* Navigate back to your Azure Portal home screen. 




a
a
a
a
a
a

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
