
const requestContract = {
    petrol_price: 10000,
    num_iteration: 500,
    max_duration: 20,
    efficiency: 12,
    capacity: 12,
    destinations: [
        {
            id: '13123124123',
            lat_lng: '3123123,123123'
        }
    ]
}

const responseContract = {
    'status': 'OK',
    'user_message': 'Aman',
    'distance': 122,
    'petrol_usage': 10,
    'petrol_price': 12000,
    route: [0,1,2,3,4,0],
}