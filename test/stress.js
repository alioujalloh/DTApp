import http from 'k6/http';
import { check } from 'k6';

// Open the file once in the init stage
const terraformFileContent = open('./../your_terraform_stae.json', 'b');

export let options = {
    vus: 1,
    duration: '1s',
};

export default function() {
    switch (__ENV.ENDPOINT) {
        case 'getall':
        case 'attribute_value_filter':
        case 'attribute_key_and_value_filter':
            testUploadWithParams({
                filterValue: __ENV.FILTER_VALUE,
                attributeKey: __ENV.ATTRIBUTE_KEY,
                attributeValue: __ENV.ATTRIBUTE_VALUE,
            });
            break;
        default:
            console.log('Please specify a valid endpoint to test.');
            break;
    }
}

function testUploadWithParams({ filterValue, attributeKey, attributeValue }) {
    let params = {};

    let url = "http://dt-app.info:8080/upload";

    // Query parameters
    let queryParams = [];
    if (filterValue) queryParams.push(`attribute_filter=${filterValue}`);
    if (attributeKey) queryParams.push(`attribute_key=${attributeKey}`);
    if (attributeValue) queryParams.push(`attribute_value=${attributeValue}`);
    if (queryParams.length > 0) url += `?${queryParams.join("&")}`;

    // Prepare the payload
    let formData = {
        file: http.file(terraformFileContent, '../your_terraform_stae.json'),
    };

    let res = http.post(url, formData, params);
    
    checkResponse(res);
}

function checkResponse(res) {
    if (res.status !== 200) {
        console.error(`Request failed with status ${res.status}: ${res.body}`);
    }

    check(res, {
        'is status 200': (r) => r.status === 200,
    });
}
