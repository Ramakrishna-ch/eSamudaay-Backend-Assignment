from werkzeug import exceptions as e

def calculate_total_order(request_param):
    Total_order_cost=0                             # Declaring and Initialising the total cost, items total,
    Item_total=0                                   # delivery fee, discount variables
    Delivery_fee=0
    Discount=0


    if "order_items" not in request_param:
        raise e.BadRequest(description="order_items parameter missing")   # @throws Http exception if order_items parameter is missing
        
    for Item in request_param["order_items"]:      # iterating through each item
        Item_total+=Item["quantity"]*Item["price"] # calculating each item's total cost by multiplying item price with its quantity
                                                   # and adding each item's total cost to Items total

    Total_order_cost+=Item_total                   # adding Items total cost to Total order cost



    Delivery_cost_slab={0:50,1:100,2:500,3:1000}   # Delivery cost slab in Rupees based on Distance in Km

    if "distance" not in request_param:
        raise e.BadRequest(description="Distance parameter missing")   # @throws Http exception if distance parameter is missing
    
    Distance_in_mt=request_param["distance"]

    if Distance_in_mt < 0 or Distance_in_mt > 500000:
        raise e.BadRequest(description="Provide Distance value between 0 and 500000")   # @throws Http exception if distance given is not in range of 0 and 500000

    Distance_in_km=Distance_in_mt/1000  # Conversion of given distance in meters to Km

    if Distance_in_km>=0 and Distance_in_km<=10:    # choosing delivery cost based on given distance in Km
        Delivery_fee=Delivery_cost_slab[0]
    elif Distance_in_km>10 and Distance_in_km<=20:
        Delivery_fee=Delivery_cost_slab[1]
    elif Distance_in_km>20 and Distance_in_km<=50:
        Delivery_fee=Delivery_cost_slab[2]
    elif Distance_in_km>50:
        Delivery_fee=Delivery_cost_slab[3]
    else:
        Delivery_fee=0

    Total_order_cost+=Delivery_fee*100            # conversion of delivery fee in Rupees to Paise and adding it to Total order cost



    if "offer" in request_param.keys():           # check if Offer is Applicable
        offer_price=0                             
        if request_param["offer"]["offer_type"] == "FLAT":       # offer price will be the given offer val, if offer type is FLAT 
            offer_price=request_param["offer"]["offer_val"]
        elif request_param["offer"]["offer_type"] == "DELIVERY": # offer price will be Delivery fee, if offer type is DELIVERY 
            offer_price=Delivery_fee
    
        Discount=min(offer_price,Total_order_cost)               # Final Discount will be offer price, if it's less than Total order cost
                                                                 # else discount will be Total order cost

    
    Total_order_cost=Total_order_cost-Discount    # Calculating Total order cost by deducing discount from it.


    response={                                   # Response message structure
        "order_total":Total_order_cost
    }

    return response                               # Returning the response message