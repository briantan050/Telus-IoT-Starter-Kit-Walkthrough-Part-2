# Telus IoT Starter Kit Walkthrough: Part 2

This is part 2 of a 3-part tutorial that will help get you started with the TELUS LTE-M IoT Starter Kit:
* **[Part 1](https://github.com/briantan050/Telus-IoT-Starter-Kit-Walkthrough-Part-1/)** will give you some background on the kit and walk you through the process of getting the kit configured to send data to your own Microsoft Azure instance.
* **[Part 2](https://github.com/briantan050/Telus-IoT-Starter-Kit-Walkthrough-Part-2/)** will walk you through using the IoT data in a logic app with the Copernicus open access hub API. 
* **[Part 3](https://github.com/briantan050/Telus-IoT-Starter-Kit-Walkthrough-Part-3/)** will walk you through displaying the IoT data in a Power BI dashboard.

### Logic app functions
Now that you have sensor data being sent to your Azure IoT Hub, it would be useful to perform automated actions on it when certain criteria is met. Logic apps allow you to perform automated workflows and functions with your data and apps. This tutorial will walk you through the process of creating a Logic App with your IoT data. 

The goal of this app will be to automatically download recent satellite imagery from given GPS coordinates from [Copernicus Open Access Hub](https://scihub.copernicus.eu/) when certain criteria is met. The Logic App will decode the IoT data, filter for a certain condition, send GPS coordinates to the connected Copernicus API, and retrieve the URL to download the satellite mapsheet. 

The list of steps is as follows:
* Create a python function to query Copernicus
* Create a Logic App
* Configure the Logic App to parse the sensor data
* Configure the Logic App to run the python function when a condition is met

### Requirements
1. [Telus IOT Starter Kit](https://www.avnet.com/shop/us/products/avnet-engineering-services/aes-bg96-iot-sk2-g-3074457345636408150?INTCMP=tbs_low-power-wide-area_button_buy-your-kit)
2. [Microsoft Azure Account](https://azure.microsoft.com/en-ca/)
3. [Copernicus Open Access Hub Account](https://scihub.copernicus.eu/dhus/#/self-registration) (free to register)
4. [Visual Studio Code](https://code.visualstudio.com/)
5. [Azure Functions Core Tools, version 3.x](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools)
6. [Python version supported by Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/supported-languages#languages-by-runtime-version). I used [Python 3.9.12](https://www.python.org/downloads/release/python-3912/)
7. [Python extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
8. [Azure Functions extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
9. Basic knowledge of Python is an asset

# Create a python function to query Copernicus
We will start by creating an Azure Function to query Copernicus Open Access Hub. Microsoft Azure allows us to create Azure Functions using Python scripts as long as we use the specific Visual Studio Code extensions. 

1. Open Visual Studio Code (VSC)
2. If you have trouble opening VSC, you can also right click on a basic text file and open with VSC.
* <img src="https://user-images.githubusercontent.com/53897474/167527349-f34fb553-9255-4fee-9555-ca0b61181d73.png" width="200" height="200">
3. Choose the Azure icon in the Activity bar, then in the Azure: Functions area, select the Create new project... icon.
4. <img src="https://user-images.githubusercontent.com/53897474/167529854-452b2a1f-84e8-4ba8-8435-76e99f2729f3.png" width="200" height="200">
5. Choose a folder location for your project workspace and choose Select. It is recommended that you create a new folder or choose an empty folder as the project workspace.
6. Provide the following information at the prompts:
   *  Select a language for your function project: Choose **Python**.
   *  Select a Python alias to create a virtual environment: Choose the location of your Python interpreter.
   *  Select a template for your project's first function: Choose **HTTP trigger**.
   *  Provide a function name: Type **CopernicusFunction**.
   *  Authorization level: Choose **Anonymous**, which enables anyone to call your function endpoint.
   *  Select how you would like to open your project: Choose **Add to workspace**.
7. Using this information, Visual Studio Code generates an Azure Functions project with an HTTP trigger. You can view the local project files in the Explorer.

# Configure the python function
The project is now ready for configuration. We will configure the python script `__init__.py` before deploying it as an Azure function.
<img src="https://user-images.githubusercontent.com/53897474/167694888-00a97e1a-ea5c-4a34-94fa-fc7e15f1be79.png" width="200" height="200">

1. Add the modules `sentinelsat` and `datetime`, which we need for the API. At the top of `__init__.py`, add the following code:
   ```
   from sentinelsat import SentinelAPI
   ```
   <img src="https://user-images.githubusercontent.com/53897474/167697641-0f2b8a66-db47-4281-924e-9de574348d05.png" width="200" height="200">

2. Add the `sentinelsat` and `pandas` module into the `requirements.txt` file so that the environment will download these modules when running the function:
   ```
   sentinelsat
   pandas
   ```
   <img src="https://user-images.githubusercontent.com/53897474/167697804-e74271ce-6401-4c4d-8a7c-b199e7f5ffd5.png" width="200" height="200">

3. We can now begin to change the script to suit our objectives. We will be counting on the When using the Copernicus API, we need to provide our login credentials. Under the `if name:` statement, add the following statement to provide your login details:
   ```
   # login to Copernicus
   api = SentinelAPI('username123', 'password123', 'https://apihub.copernicus.eu/apihub')
   ```
   <img src="https://user-images.githubusercontent.com/53897474/167698858-81462527-3464-4388-a30f-ae4d827f3f68.png" width="200" height="200">

4. Add the following statement:
   ```
   # query
   latlong = name
   products = api.query(footprint="intersects({})".format(latlong),
                       date=('NOW-5DAYS', 'NOW'))
   ```
   <img src="https://user-images.githubusercontent.com/53897474/167702879-639c75ea-0963-4c89-99bc-88ebef5138fd.png" width="200" height="200">

5. Add the following statement:
   ```
   # convert to pandas
   products_df = api.to_dataframe(products)

   # sort
   sort = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
        
   # choose top one
   top_one = sort.head(1)
   map_id = top_one.index.values
   ```
   <img src="https://user-images.githubusercontent.com/53897474/167703074-3e854acd-1f3d-48c7-9786-b9257fcdb519.png" width="200" height="200">

6. Add the following statement:
   ```
   # get metadata
   map_metadata = api.get_product_odata(map_id[0])
   title = map_metadata['title']
   size = map_metadata['size']
   date = map_metadata['date']
   url = map_metadata['url']
   creation_date = map_metadata['Creation Date']
   ingestion_date = map_metadata['Ingestion Date']
   quicklook_url = map_metadata['quicklook_url']
   ```
   <img src="https://user-images.githubusercontent.com/53897474/167703560-33013e31-0eff-4420-b432-51c5417bdc4a.png" width="200" height="200">

   
7. Add the following statement:
   ```
   return func.HttpResponse(f'{{"map_id":"{map_id}","title":"{title}","size":"{size}","date":"{date}","url":"{url}","creation_date":"{creation_date}","ingestion_date":"{ingestion_date}","quicklook_url":"{quicklook_url}"}}')
   ```
   <img src="https://user-images.githubusercontent.com/53897474/167703761-011c82fb-7f1e-4713-b1da-8eafcb08b714.png" width="200" height="200">

8. Press F5 to run and start debugging. If all goes well, it should look like the following image:
   <img src="https://user-images.githubusercontent.com/53897474/167704312-9bb36e73-3a73-4bd9-bf72-ac8a87a79589.png" width="200" height="200">
   I sometimes run into the problem of VSC being unable to load the correct Python version (3.9.12) despite setting version already. I simply press F5 to run and start debugging a couple more times until it works again. 
   
9. Now that the function is running locally, go back to the Azure extension, and run the CopernicusFunction HTTP web hook. 
<img src="https://user-images.githubusercontent.com/53897474/167705136-2dc7cf2d-4b07-4362-93aa-b607a4b27c2a.png" width="200" height="200">

10. Replace **Azure** with the test coordinates **73.000, -123.000** and press Enter to see if the function works. 
<img src="https://user-images.githubusercontent.com/53897474/167705247-10b13bdb-ae9c-420b-9496-9a6a5e8b0d28.png" width="200" height="200">

11. The function queries Copernicus successfully. Click the **Deploy to Function App** button to deploy it to Azure as a Function App. You can create a new Function App in Azure, or overwrite an existing one.
<img src="https://user-images.githubusercontent.com/53897474/167706032-1e3c572a-b7e4-476b-af3b-ce5c64e2aa0e.png" width="200" height="200">

12. Done! You have successfully created an Azure Function App from a python script! 


   
# Create a Logic App
1. In the Azure portal, select **Create a resource**. 
2. Type **Logic app** in the search box and select it from the drop-down list. 
3. On the Logic app overview page, select **Create**
4. Enter the following information for the Logic app:  

* **Subscription**: Select your existing subscription or create a new one.
* **Resource Group**: Select your existing Resource Group or create a new one.
* **Logic App name**: Choose a name for your Logic App. This can be anything.
* **Region**: Use the same location as your resource group.
* **Enable log analytics**: Select **No**
* **Plan type**: Select **Consumption**

<img src="https://user-images.githubusercontent.com/53897474/167044055-bd428dd2-c926-423c-8878-46029cd6ddb3.png" width="200" height="200">

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
<img src="https://user-images.githubusercontent.com/53897474/167047536-f6fed635-8d10-4ec4-ae65-896e5c93d189.png" width="200" height="200">
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
* Microsoft Azure's tutorial: [Quickstart: Create a function in Azure with Python using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
* Dinusha Kumarasiri's tutorial: [End to end IoT Solution with Azure IoT Hub, Event Grid and Logic Apps](https://youtu.be/Wb_QT0qHGOo)
* Reza Vahidnia and F. John Dian's book: [Cellular Internet of Things for Practitioners](https://pressbooks.bccampus.ca/cellulariot/)
