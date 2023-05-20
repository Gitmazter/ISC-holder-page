<h1> Server Usage </h1>

<h2> Step 1 </h2>
<p>
Clone repo into local directory
</p>
<blockquote>
gh repo clone Gitmazter/ISC-holder-page
</blockquote>
<hr/>
<h2> Step 2 </h2>
<p>
Add .env to the root folder with the following keys:
</p>
<blockquote>
MONGO_DB_UN = Your Mongo Db Username <br/> 
MONGO_DB_KEY = You Mongo Db Database Password<br/> 
TOKEN_ADDRESS = Blockchain Address For Yout Token Contract<br/>
MINT AUTHORITY = Blockchain Address For The Mint Authority Of Your Token<br/>
SOLSCAN_API_KEY = Your Solscan API key<br/>
</blockquote>
<hr/>
<h2> Step 3 </h2>
<p>
Install all dependecies if not already installed:
</p>
<blockquote>
    pip install pymongo \<br/>
    pip install flask \<br/>
    pip install pyngrok
</blockquote>

<hr/>
<h2> Step 4 </h2>
<p>
From root run the main function to initialize DB and collect data <br/>
</p>
<blockquote>
    python3 main.py
</blockquote>
<br/>
<h4>
<b>**WARNING**</b> <u>updating users and transactions may take a long time due to Solcan API limitations! </u> <br/>
</h4>
<hr/>
<h2> Step 5 </h2>
<p>
Once the DB has been initialized and updated, start the server locally at your port of choice (*Select Port at end of Server.py file*) by typing the command, this is done in the root folder:
</p>
<blockquote>
    python3 server.py
</blockquote>
<hr/>
<h2> Step 6 </h2>
<p>
Open a new terminal and cd into the project root folder then type the command 
</p>
<blockquote>
    ngrok http *Your Port*
</blockquote>
<hr/>
<h2> Step 6 </h2>
<p>
In the terminal running the ngrok service, a link will be displayed besides "Forwarding", this link will take you to your live API server.
To test, try the following URL
</p>
<blockquote>
    https://"NGROK_URL"/igtBalance/?address="Your Pubkey"
</blockquote>
<hr/>