import Centrifuge from "centrifuge";

import songService from "./songService";

const connect = () => {
  // initialize store
  songService.getSongs();

  const centrifuge = new Centrifuge(
    "wss://realtime.zuri.chat/connection/websocket"
  );

  centrifuge.subscribe("zuri-plugin-music", (message) => console.log(message));

  centrifuge.on("connect", (context) => {
    // console.log(context);
  });

  centrifuge.connect();
};

export default { connect };
