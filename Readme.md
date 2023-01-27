# Lang & Schwarz TradeCenter  API
The goal of this project is to receive the live data from the [Lang & Schwarz TradeCenter](https://www.ls-tc.de/) using the [Lightstreamer Protocol](https://lightstreamer.com/). 

## The protocol
1. The client sends a request to `/lightstreamer/create_session.js` to create a session. The `LS_adapter_set` must be `WALLSTREETONLINE` and the `LS_phase` a random number.
2. The server will answer with a response that contains the session key. 
3. Next, the client sends a request to open a websocket.
4. Using this socket, the client tries to bind the session, sending the `bind_session` command togehter with its `LS_phase` and the session key. However, instead of the response I get on the website, I receive the following content which probably means that someting went wrong: `setPhase(<LS_phase>);retry();`. Unfortunatly, I don't know why...

Any contribution to this project is welcome. Thanks!