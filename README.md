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
We will start by creating an Azure Function app to query Copernicus Open Access Hub. Microsoft Azure allows us to create Azure Functions deployed from a Python script as long as we use the specific Visual Studio Code extensions. 

1. Open Visual Studio Code (VSC)
2. Choose the Azure icon in the Activity bar, Sign into Azure. This will open a browser window for you to sign into Azure.  
   <img src="https://user-images.githubusercontent.com/53897474/168380923-f1f7b937-c37b-4952-8290-eabad28e2643.png" width="400">

3. Once signed in, back in VSCode select the **Create new project...** icon.  
   <img src="https://user-images.githubusercontent.com/53897474/168380923-f1f7b937-c37b-4952-8290-eabad28e2643.png" width="400">
   
4. Choose a folder location for your project workspace and choose Select. It is recommended that you create a new folder or choose an empty folder as the project workspace.
5.  Provide the following information at the prompts:
   *  Select a language for your function project: Choose **Python**.
   *  Select a Python alias to create a virtual environment: Choose py -3.9 or the folder location of your python 3.9.12.  
      <img src="https://user-images.githubusercontent.com/53897474/168383264-b0f3c9b2-fae1-4379-886c-dece7a185e76.png" width="400">

   *  Select a template for your project's first function: Choose **HTTP trigger**.
   *  Provide a function name: Type **CopernicusFunction**.
   *  Authorization level: Choose **Anonymous**, which enables anyone to call your function endpoint.
   *  Select how you would like to open your project: Choose **Add to workspace**.
6. Using this information, Visual Studio Code generates an Azure Functions project with an HTTP trigger. You can view the local project files in the Explorer.

# Configure the python function
The python script is now ready to be configured to suit our purpose. The following instructions outline how to the python script `__init__.py` before deploying it as an Azure function, however, I have added my copy for your convenience, but you will still need to change the **username123** and **password123** fields, as well as the `requirements.txt` file. 

This is what it looks like to start:  
<img src="https://user-images.githubusercontent.com/53897474/167694888-00a97e1a-ea5c-4a34-94fa-fc7e15f1be79.png" width="900">

1. Add the module `sentinelsat`, which is the module that connects to the Copernicus Open Data Hub. At `line 5` add the following code:
   ```
   from sentinelsat import SentinelAPI
   ```
<img src="https://user-images.githubusercontent.com/53897474/167697641-0f2b8a66-db47-4281-924e-9de574348d05.png" width="900">

2. Add the required modules into the `requirements.txt` file so that the environment will download these modules when running the function. We need the `pandas` module in order to sort through the results from querying the map list later on. In the `requirements.txt` file, add the following statement:
   ```
   sentinelsat
   pandas
   ```
<img src="https://user-images.githubusercontent.com/53897474/167697804-e74271ce-6401-4c4d-8a7c-b199e7f5ffd5.png" width="900">

3. Connect to Copernicus Open Access Hub with your login credentials using the API. At `line 20`, add the following statement and replace **username123** and **password123** with your own details:
   ```
   # login to Copernicus
   api = SentinelAPI('username123', 'password123', 'https://apihub.copernicus.eu/apihub')
   ```
<img src="https://user-images.githubusercontent.com/53897474/167698858-81462527-3464-4388-a30f-ae4d827f3f68.png" width="900">

4. Add the following statement:
   ```
   # query
   latlong = name
   products = api.query(footprint="intersects({})".format(latlong),
                       date=('NOW-5DAYS', 'NOW'))
   ```
<img src="https://user-images.githubusercontent.com/53897474/167702879-639c75ea-0963-4c89-99bc-88ebef5138fd.png" width="900">

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
<img src="https://user-images.githubusercontent.com/53897474/167703074-3e854acd-1f3d-48c7-9786-b9257fcdb519.png" width="900">

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
<img src="https://user-images.githubusercontent.com/53897474/167703560-33013e31-0eff-4420-b432-51c5417bdc4a.png" width="900">
   
7. Add the following statement:
   ```
   return func.HttpResponse(f'{{"map_id":"{map_id}","title":"{title}","size":"{size}","date":"{date}","url":"{url}","creation_date":"{creation_date}","ingestion_date":"{ingestion_date}","quicklook_url":"{quicklook_url}"}}')
   ```
<img src="https://user-images.githubusercontent.com/53897474/167703761-011c82fb-7f1e-4713-b1da-8eafcb08b714.png" width="900">

8. Press F5 to run and start debugging. If all goes well, it should look like the following image:
<img src="https://user-images.githubusercontent.com/53897474/167704312-9bb36e73-3a73-4bd9-bf72-ac8a87a79589.png" width="900">  
   I sometimes run into the problem of VSC being unable to load the correct Python version (3.9.12) despite setting version already. I simply press F5 to run and start debugging a couple more times until it works again. 
   
9. Now that the function is running locally, go back to the Azure extension, and run the CopernicusFunction HTTP trigger. 
<img src="https://user-images.githubusercontent.com/53897474/167705136-2dc7cf2d-4b07-4362-93aa-b607a4b27c2a.png" width="900">

10. Replace **"Azure"** with some test coordinates such as **"73.000, -123.000"** and press Enter to see if the function works. 
<img src="https://user-images.githubusercontent.com/53897474/167705247-10b13bdb-ae9c-420b-9496-9a6a5e8b0d28.png" width="900">

11. The function queries Copernicus successfully. Click the **Deploy to Function App** button to deploy it to Azure as a Function App. You can create a new Function App in Azure, or overwrite an existing one.
<img src="https://user-images.githubusercontent.com/53897474/167706032-1e3c572a-b7e4-476b-af3b-ce5c64e2aa0e.png" width="900">

12. Done! You have successfully created an Azure Function App from a python script!

# Create a Logic App
Now we will create a logic app. 
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
<img src="https://user-images.githubusercontent.com/53897474/167044055-bd428dd2-c926-423c-8878-46029cd6ddb3.png" width="600">

5. Select **Review + Create**, and then **Create**.

# Configure the Logic App
Now we will configure the Logic App to receive the message payload from your Azure IoT Hub. 
1. Open the Logic App.
2. Scroll down and select **When a HTTP request is received**.
<img src="https://user-images.githubusercontent.com/53897474/167739956-fe95c36a-e7b6-47bb-9674-1bb1669787d4.png" width="600"> 

3. On the top toolbar, select **Code view**.
<img src="https://user-images.githubusercontent.com/53897474/167740066-5624ed96-5c25-4138-ba30-df846f138b7e.png" width="600">

4. Replace the existing code with the code from **logic_app.txt**. 
5. At the top toolbar, select **Save**.
6. At the top toolbar, select **Designer** to open the design view.
7. Select the first block, the Trigger, to open it.
8. Copy the **HTTP POST URL**. We will need it for the next step.  
<img src="https://user-images.githubusercontent.com/53897474/167047536-f6fed635-8d10-4ec4-ae65-896e5c93d189.png" width="600">
9. Navigate back to your Azure Portal home screen.

# Create a subscription event
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

# Verify that the Logic App runs successfully
1. Open the Logic App.
2. Turn on the Microcontroller and start receiving the data payloads. They should start to appear in the Logic App Overview. Click on a successful run to open up the Run History. 
<img src="https://user-images.githubusercontent.com/53897474/168176976-ba205a44-ac71-410e-986f-b60d40b4ac6f.png" width="600">
3. In the run history, you can inspect the details of the successful run. Scrolling down to **Parse JSON telemetry string** would show the received data payload from the sensor.
<img src="https://user-images.githubusercontent.com/53897474/168177160-59bd1641-048d-48c1-b58c-a867749a9056.png" width="600">

4. Navigate back to the Logic App Designer.

# Configure the Logic App
We will now configure the Logic App to execute your created Azure Function when a condition is met. For this tutorial, the condition is already set to **ButtonPress = 0**, signifying that the button has not been pressed. 
1. In the Logic App Designer, scroll down to **Condition** and click to open.
2. On the **True** block, click **Add Action**. 
3. Search for **Azure Function** and add it to the workflow. Your created Azure Function should appear. 
<img src="https://user-images.githubusercontent.com/53897474/168180743-06eebbf4-edc6-483a-8d4b-2d61b69d8062.png" width="600">

4. Set the **Request Body** to **latlong**
<img src="https://user-images.githubusercontent.com/53897474/168183754-d945c083-3d60-4b7d-a9ee-56ae43b82086.png" width="600">

5. Create a new action by selecting **Add an action**. 
6. Search for the **Parse JSON** built-in operation and select it. 
<img src="https://user-images.githubusercontent.com/53897474/168183997-2822e4a9-2b7d-41b2-a853-30b33ffdb6dd.png" width="600">

7. For **Content**, choose **Body** from your your created Azure Function. 
8. For **Schema**, copy and paste the code from `parse_JSON_schema.txt`.
<img src="https://user-images.githubusercontent.com/53897474/168335305-f90e1e9c-2f14-4b1a-8661-fd7cb0c558ad.png" width="600">

9. Add another action by selecting **Add an action**.
10. Search for **Outlook**, and choose **Send an email (V2)**
<img src="https://user-images.githubusercontent.com/53897474/168336330-10bf17d9-2deb-42df-bc92-9760b0b14ae7.png" width="600">

11. It will prompt you to sign in to create a connection to Outlook.com. Sign in and accept the permissions. You could also make a new Outlook email account specifically for this purpose just to test it out.
12. Configure the **Send an email** function as follows:
* **Body**: copy and paste the code from `email_body.txt`. 
* **Subject**: Give it a subject, this could be anything.
* **To**: Type out the email you want to send the alert to. 

13. At the top left, click **Save**.

# Verify that the Logic App works correctly
1. Navigate to the Logic App Overview
2. Click on a succeeded run
3. Click **Resubmit** to run the payload again with the new changes to the logic app.
<img src="https://user-images.githubusercontent.com/53897474/168349096-b0270a96-fdcf-4e29-b842-cc7f1bd6fc37.png" width="600">

4. Click **Refresh** to see the new run appear. Click it and scroll down to follow its progress in real time. 
5. The Logic App should run, detect that the button was not pressed (ButtonPress = 0), and send the email to your inbox.

## Done
You are now using an Azure Logic App to process data payloads and receive metadata of recent satellite imagery of the area. In this tutorial, you have completed the following:
* Create and configure an Azure Function using Python
* Create an Azure Logic App
* Configure the Logic App to run the Azure Function and send an email when a specific criteria is met

## Next steps
If you are interested in displaying the IoT data in a Power BI dashboard, continue on to **[Part 3](https://github.com/briantan050/Telus-IoT-Starter-Kit-Walkthrough-Part-3/)**.

## Credits:
* GarettB's tutorial: [TELUS IOT Getting Started](https://github.com/garettB/TELUS_IoT_Getting_Started)
* Microsoft Azure's tutorial: [Visualize real-time sensor data from Azure IoT Hub using Power BI](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-live-data-visualization-in-power-bi)
* Microsoft Azure's tutorial: [Quickstart: Create a function in Azure with Python using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
* Dinusha Kumarasiri's tutorial: [End to end IoT Solution with Azure IoT Hub, Event Grid and Logic Apps](https://youtu.be/Wb_QT0qHGOo)
* Reza Vahidnia and F. John Dian's book: [Cellular Internet of Things for Practitioners](https://pressbooks.bccampus.ca/cellulariot/)
