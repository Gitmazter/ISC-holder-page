import  http  from 'http'
import  fs  from 'fs'
import Holder from './classes/holder.js';
import { fetchISCMeta, fetchISCHolders } from './services/Solscan.js';

let holders = '{}';

var server = http.createServer(async function (req, res) {   
    if (req.url == '/holder-data') { //check the URL of the current request
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.write(holders) 
        res.end();
    }
});
server.listen(5000);

console.log('Node.js web server at port 5000 is running..');

// Writes fetched data to JSON file
const writeHolders = async () => {
    //console.log('fetching data....');
    const holderData = await calculateStakes();
    //console.log(holderData);
    //console.log("writing file....");
    fs.writeFileSync("holders.json", JSON.stringify(holderData));
}
setInterval(writeHolders, 5000)

const loadHolders = async () => {
    fs.readFile("./holders.json", "utf8", (err, jsonString) => {
        if (err) {
          console.log("File read failed:", err);
          return;
        }
        //console.log('updating holders...');
        holders = jsonString;
    });
}
setInterval(loadHolders, 5000)


const calculateStakes = async () => {
    const holdersJsonData = await fetchISCHolders();
    const holdersData = holdersJsonData.data;
    const meta = await fetchISCMeta();
    const supply = meta.supply;


    const holdersArray = holdersData.map((holder) => {
        return (new Holder(holder.address, holder.amount, holder.owner, true, supply));
    })
    return holdersArray;
}
//calculateStakes();
