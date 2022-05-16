import logging

import azure.functions as func

from sentinelsat import SentinelAPI

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        # authy
        api = SentinelAPI('username123', 'password123', 'https://apihub.copernicus.eu/apihub')
        
        # query
        latlong = name
        products = api.query(footprint="intersects({})".format(latlong),
                            date=('NOW-5DAYS', 'NOW'))
        
        # convert to pandas
        products_df = api.to_dataframe(products)

        # sort
        sort = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
        
        # choose top one
        top_one = sort.head(1)
        map_id = top_one.index.values

        # get metadata
        map_metadata = api.get_product_odata(map_id[0])
        title = map_metadata['title']
        size = map_metadata['size']
        date = map_metadata['date']
        url = map_metadata['url']
        creation_date = map_metadata['Creation Date']
        ingestion_date = map_metadata['Ingestion Date']
        quicklook_url = map_metadata['quicklook_url']

        return func.HttpResponse(f'{{"map_id":"{map_id}","title":"{title}","size":"{size}","date":"{date}","url":"{url}","creation_date":"{creation_date}","ingestion_date":"{ingestion_date}","quicklook_url":"{quicklook_url}"}}')
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
