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

1. Open **Visual Studio Code** (VSC)
2. Choose the **Azure icon** in the Activity bar, **Sign into Azure**. This will open a browser window for you to sign into Azure.  
   <img src="https://user-images.githubusercontent.com/53897474/168636078-ec75afe2-a90c-4203-aadb-6d99990b6ac4.png" width="300">

___

3. Once signed in, back in VSCode select the **Create new project...** icon.  
   <img src="https://user-images.githubusercontent.com/53897474/168636244-ca353ce6-66ea-492b-a42b-6eb24c972c6b.png" width="300">

___

4. Choose a folder location for your project workspace and choose **Select**. It is recommended that you create a new folder or choose an empty folder as the project workspace.
5.  Provide the following information at the prompts:
   *  Select a language for your function project: Choose **Python**.
   *  Select a Python alias to create a virtual environment: Choose **py -3.9** or the folder location of your python 3.9.12.  
      <img src="https://user-images.githubusercontent.com/53897474/168636384-6d6270a1-2134-41f5-a517-4073482ecfc7.png" width="600">

   *  Select a template for your project's first function: Choose **HTTP trigger**.
   *  Provide a function name: Type **CopernicusFunction**.
   *  Authorization level: Choose **Anonymous**, which enables anyone to call your function endpoint.
   *  Select how you would like to open your project: Choose **Add to workspace**.
6. Using this information, Visual Studio Code generates an Azure Functions project with an HTTP trigger. You can view the local project files in the Explorer.

# Configure the python function
The python script is now ready to be configured to suit our purpose. The following instructions outline how to the python script `__init__.py` before deploying it as an Azure function, however, I have added my copy for your convenience, but you will still need to change the **username123** and **password123** fields, as well as the `requirements.txt` file. 

This is what it looks like to start:  
<img src="https://user-images.githubusercontent.com/53897474/168637491-4ab0a4cb-9288-4569-a1b6-c1c037ac281a.png" width="1000">

___

1. Add the module `sentinelsat`, which is the module that connects to the Copernicus Open Data Hub.  
   At `line 5` add the following code:
   ```
   from sentinelsat import SentinelAPI
   ```
<img src="https://user-images.githubusercontent.com/53897474/168636844-0b4f8126-a5af-46f2-b114-a417664f73cf.png" width="950">

___

2. Add the required modules into the `requirements.txt` file so that the environment will download these modules when running the function. We need the `pandas` module in order to sort through the results from querying the map list later on.  
   In the `requirements.txt` file, add the following code:
   ```
   sentinelsat
   pandas
   ```
<img src="https://user-images.githubusercontent.com/53897474/168637254-00217cc8-3906-45c7-92c6-668adac256a7.png" width="950">

___

3. Add your login credentials to login to Copernicus Open Access Hub with the API.  
   Back in the `__init__.py` file, at `line 20`, add the following code and replace **username123** and **password123** with your own details:
   ```
   # login to Copernicus
   api = SentinelAPI('username123', 'password123', 'https://apihub.copernicus.eu/apihub')
   ```
   * `line 10` checks for the object `name`, and if it has been set by the user, will execute the section under `line 19`.  
<img src="https://user-images.githubusercontent.com/53897474/168637858-400677e7-4e49-40e6-b803-c9e50d758160.png" width="950">

___

4. Query Copernicus Open Access Hub using the latlong coordinates.  
   At `line 23`, add the following code:
   ```
   # query
   latlong = name
   products = api.query(footprint="intersects({})".format(latlong),
                       date=('NOW-5DAYS', 'NOW'))
   ```
   * We use `latlong = name` because later in the tutorial, the latlong coordinates are stored as a variable called `name`. 
   * `api.query` is the function to query the map products on Copernicus Open Access Hub.
   * We use `footprint="intersects({})".format(latlong)` to filter for map products which intersect our given latlong coordinate.
   * We use `date=('NOW-5DAYS', 'NOW')` to filter for map products posted between 5 days ago to today.
   * To construct your own queries, more documentation on the syntax is available in [this link](https://scihub.copernicus.eu/userguide/FullTextSearch), although some trial and error is involved as it does not outline how to use the queries with python completely. 
<img src="https://user-images.githubusercontent.com/53897474/168638069-aa902c47-f9fd-45e0-9f55-86cdcd3d98f6.png" width="950">

___

5. Convert the query of map products into a dataframe, sort it, and choose the top result.  
   At `line 28`, add the following code:
   ```
   # convert to pandas
   products_df = api.to_dataframe(products)

   # sort
   sort = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
        
   # choose top one
   top_one = sort.head(1)
   map_id = top_one.index.values
   ```
   * We convert our query of map products into a pandas dataframe as it makes it simpler to sort.
   * We sort it by cloud cover percentage and date in ascending order.
   * We use `sort.head(1)` to choose the single top map product that appears at the top of the sorted dataframe. 
   * We use `index.values` to fetch the map ID of the map product.
<img src="https://user-images.githubusercontent.com/53897474/168639124-f649d363-315f-49c8-b024-b48d3abeba6d.png" width="950">

___

6. Grab the metadata using the map ID from the previous step, and store them as objects.  
   At `line 38`, add the following code:
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
<img src="https://user-images.githubusercontent.com/53897474/168640109-72134607-27a9-410d-a3af-975c09213efd.png" width="950">

___

7. Print the metadata in JSON format using an f string.  
   At `line 48`, add the following code:
   ```
   return func.HttpResponse(f'{{"map_id":"{map_id}","title":"{title}","size":"{size}","date":"{date}","url":"{url}","creation_date":"{creation_date}","ingestion_date":"{ingestion_date}","quicklook_url":"{quicklook_url}"}}')
   ```
<img src="https://user-images.githubusercontent.com/53897474/168640367-89ad3aba-a810-4c43-9059-859414049052.png" width="950">

___

8. Press F5 to run and start debugging. I sometimes run into the problem of VSCode being unable to load the correct Python version **(3.9.12)** despite already setting the version. I simply press F5 to run and start debugging a few more times until it works again.  
   If all goes well, it should look like the following image:  
<img src="https://user-images.githubusercontent.com/53897474/167704312-9bb36e73-3a73-4bd9-bf72-ac8a87a79589.png" width="950">  

___

9. Now that the function is running locally, go back to the **Azure extension**, and run the **CopernicusFunction** HTTP trigger. 
<img src="https://user-images.githubusercontent.com/53897474/168641049-34b8ab39-5124-41a6-b41f-c2a38a664916.png" width="950">

___

10. Replace **"Azure"** with some test coordinates such as **"73.000, -123.000"** and press Enter to see if the function works. 
<img src="https://user-images.githubusercontent.com/53897474/168641200-1757abd5-65e2-46ba-ac7d-29b37163e40c.png" width="950">

___

11. The function queries Copernicus successfully. Click the **Deploy to Function App** button to deploy it to Azure as a Function App. You can create a new Function App in Azure, or overwrite an existing one.
<img src="https://user-images.githubusercontent.com/53897474/168641383-4d05e4de-8819-4048-bd20-2049da90025b.png" width="950">

___

12. Done! You have successfully created an Azure Function App from a python script!

# Create a Logic App
Now we will create a logic app to construct an automated workflow. 
1. In the Azure portal, select **Create a resource**. 
2. Type **Logic app** in the search box and select it from the drop-down list. 
3. On the Logic app overview page, select **Create**.
4. Enter the following information for the Logic app: 
* **Subscription**: Select your existing subscription or create a new one.
* **Resource Group**: Select your existing Resource Group or create a new one.
* **Logic App name**: Choose a name for your Logic App. This can be anything.
* **Region**: Use the same location as your resource group.
* **Enable log analytics**: Select **No**
* **Plan type**: Select **Consumption**
<img src="https://user-images.githubusercontent.com/53897474/168641757-8ce53b9e-7d27-487f-82aa-aca1a7eb645c.png" width="500">

5. Select **Review + Create**, and then **Create**.

# Configure the Logic App
Now we will configure the Logic App to receive the message payload from your Azure IoT Hub. This is done by creating a **HTTP request** on the Logic App, which will receive the data payload from your Azure IoT Hub.  
1. Open the Logic App.
2. Scroll down and select **When a HTTP request is received**.
<img src="https://user-images.githubusercontent.com/53897474/168641928-62f1bdcd-6a0c-488a-a2dc-e3ec25741025.png" width="600"> 

___

3. On the top toolbar, select **Code view**.
<img src="https://user-images.githubusercontent.com/53897474/168642132-224cd238-f2b7-40ca-ab63-092a2a48efd2.png" width="600">

___

4. Replace the existing code with the code from **logic_app_code.txt**. 
5. At the top toolbar, select **Save**.
6. At the top toolbar, select **Designer** to open the design view.
7. Select the first block, the Trigger, to open it.
8. Copy the **HTTP POST URL**. We will need it for the next step.  
<img src="https://user-images.githubusercontent.com/53897474/168642319-620a4689-3306-4e8a-b00e-4f9018cb948d.png" width="600">
9. Navigate back to your Azure Portal home screen.

# Create a subscription event
Now we will create a subscription event to send the data from your Azure IoT Hub to your Logic App. 
1. In the Azure portal, open your **IoT Hub**.
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

Your Azure IoT Hub and your Logic App should now be connected. Azure IoT Hub will receive the telemetry messages from your sensor, and then the event subscription will relay those messages to your designated endpoint, the Logic App. 

# Verify that the Logic App runs successfully
1. Open the **Logic App**.
2. Turn on the Microcontroller. Once the messages are being received into your IoT Hub, they should also start to appear in the Logic App Overview. Click on a successful run to open up the Run History.
<img src="https://user-images.githubusercontent.com/53897474/168642635-d0f6551d-3340-4986-82fa-f67799561c70.png" width="700">

___

3. In the **run history**, you can inspect the details of the successful run. Scrolling down to **Parse JSON telemetry string** would show the received data payload from the sensor.
<img src="https://user-images.githubusercontent.com/53897474/168642826-b6ff523b-7f4b-46d8-92fa-134a8987597a.png" width="600">

4. Navigate back to the **Logic App Designer**.

# Understanding the Logic App so far
We will now configure the Logic App to execute your created Azure Function when a condition is met. I will first explain the current workflow that has been imported from the `logic_app_code.txt` file. 
* **When a HTTP request is received**
   * This is the trigger for the Logic App. The workflow will begin once a telemetry message is received from your connected IoT Hub.
   * The telemetry message is received as an encoded message stored in the object called **body (red box)**.
   * This object is stored inside a JSON object **(green box)**.
   * This JSON object is stored inside an array **(orange box)**.
   * This array is stored inside the JSON object **(purple box)** which is generated from the current HTTP trigger. 
<img src="https://user-images.githubusercontent.com/53897474/168642941-195f39cd-eee4-4107-a0d4-eb5fc183ec07.png" width="700">

___

* **Steps 1-6**
   * These steps involve parsing the data from the **red box** to **purple box**. 

* **7. Parse JSON telemetry string**
   * This step parses the decoded telemetry string as the different data points captured by the sensor: longitude, latitude, temperature, humidity, etc. 

* **8. Initialize latlong variable**
   * This step creates a variable called **latlong**, which contains the latitude and longitude coordinates in JSON format under the title "name".  

* **9. Condition**
   * This step checks whether a certain criteria is met, and executes functions depending on whether that that criteria is true or false.
   * The current condition is set to **"ButtonPress = 0"**.  
   * To change the condition to your own criteria, you must add your desired variable from the **Dynamic Content**.
   * Because the sensor telemetry messages are imported as text strings, we will need to convert them into integers using the `int()` function.
   * For creating a condition with variable `Humidity`, you will click on the `Humidity` variable under `7. Parse JSON telemetry string`, and enclose it inside the brackets of the `int()` function.  
<img src="https://user-images.githubusercontent.com/53897474/168655095-bedb2cb2-65d7-43d3-8a5a-0f3306db842e.png" width="700">

# Add the Azure Function to the Logic App
We will now configure the Logic App to execute your Azure Function when a condition is met.  
1. In the **Logic App Designer**, scroll down to step 9, **Condition**, and click to open. The current condition is set to `ButtonPress = 0`. 
   * You can change this to other 
2. On the **True** block, click **Add Action**. 
3. Search for **Azure Function** and add it to the workflow. Your created Azure Function should appear. 
<img src="https://user-images.githubusercontent.com/53897474/168643108-fd4c802e-17c1-4bae-84b3-64268cc1f137.png" width="600">

___

4. Set the **Request Body** to **latlong**
<img src="https://user-images.githubusercontent.com/53897474/168645699-965c4017-91ce-4d78-91d2-9811c3360921.png" width="600">

The Logic App will now execute the Azure Function when it receives a telemetry message from IoT Hub where `ButtonPress = 0`. All incoming messages should therefore trigger the function so long as the Microcontroller's blue user button is not pressed.

# Parse the metadata and send an email
At this stage in the Logic App, the Azure Function has been executed and sent back the metadata of a mapsheet in JSON format. We must parse this JSON format before being able to send the metadata in an email.  
1. Create a new action below by selecting **Add an action**. 
2. Search for the **Parse JSON** built-in operation and select it. 
<img src="https://user-images.githubusercontent.com/53897474/168643716-ba41e765-ec19-49d4-a56c-57059e9257cb.png" width="600">

___

3. For **Content**, choose **Body** from your your created Azure Function. 
4. For **Schema**, copy and paste the code from `parse_JSON_schema.txt`.
<img src="https://user-images.githubusercontent.com/53897474/168644077-a80386b3-7eb8-4334-91a8-845bb00fa6a8.png" width="600">

___

We will now use the parsed metadata to construct an email. 
1. Add another action by selecting **Add an action**.
2. Search for **Outlook**, and choose **Send an email (V2)**
<img src="https://user-images.githubusercontent.com/53897474/168644274-01776dcd-92c0-43e2-b9ae-859897ca0183.png" width="600">

___

3. It will prompt you to sign in to create a connection to Outlook.com. Sign in and accept the permissions. You could also make a new Outlook email account specifically for this purpose just to test it out.
4. Configure the **Send an email** function as follows:
* **Body**: copy and paste the code from `email_body.txt`, or select your own variables from the **Dynamic content** window. 
* **Subject**: Give it a subject, this could be anything.
* **To**: Type out the email you want to send the alert to. 

5. At the top left, click **Save**.

# Verify that the Logic App works correctly
1. Navigate to the **Logic App Overview**.
2. Click on a succeeded run.
3. Click **Resubmit** to run the payload again with the new changes to the logic app.
<img src="https://user-images.githubusercontent.com/53897474/168644484-7526f378-6371-4fab-a188-92e3dc3b6e03.png" width="600">

___

4. Click **Refresh** to see the new run appear. Click it and scroll down to follow its progress in real time. 
5. The Logic App should run, detect that the button was not pressed (ButtonPress = 0), and send the email to your inbox.

## Done
You are now using an Azure Logic App to process data payloads and receive metadata of recent satellite imagery of the area. In this tutorial, you have completed the following:
* Create a python function to query Copernicus
* Create a Logic App
* Configure the Logic App to parse the sensor data
* Configure the Logic App to run the python function when a condition is met

## Next steps
* You can now configure the Logic App to your own specifications. 
* Try changing the query of the Azure Function to search for map products from a particular satellite type. 
* Try changing the Logic App condition to send an email when above a certain temperature.
* Try changing the layout of the email to notify the user about different metrics.
* If you are interested in displaying the IoT data in a Power BI dashboard, continue on to **[Part 3](https://github.com/briantan050/Telus-IoT-Starter-Kit-Walkthrough-Part-3/)**.

## Credits:
* GarettB's tutorial: [TELUS IOT Getting Started](https://github.com/garettB/TELUS_IoT_Getting_Started)
* Microsoft Azure's tutorial: [Visualize real-time sensor data from Azure IoT Hub using Power BI](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-live-data-visualization-in-power-bi)
* Microsoft Azure's tutorial: [Quickstart: Create a function in Azure with Python using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
* Dinusha Kumarasiri's tutorial: [End to end IoT Solution with Azure IoT Hub, Event Grid and Logic Apps](https://youtu.be/Wb_QT0qHGOo)
* Reza Vahidnia and F. John Dian's book: [Cellular Internet of Things for Practitioners](https://pressbooks.bccampus.ca/cellulariot/)
