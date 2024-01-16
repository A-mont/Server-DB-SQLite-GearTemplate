import React, { useState, useEffect } from "react";
import { Button } from "@chakra-ui/react";
import axios from "axios";

function PlayerList() {
  const [players, setPlayers] = useState([]);

  const fetchPlayers = async () => {
    try {
      const response = await axios.get("http://localhost:5000/players");
      setPlayers(response.data.players);

      console.log(response);
    } catch (error) {
      console.error("Error al obtener la lista de jugadores:", error);
    }
  };

  useEffect(() => {
    fetchPlayers();
  }, []);
  return (
    <div>
      <h2>Players</h2>
      <Button onClick={fetchPlayers}>Get Players</Button>
      <ul>
        {players.map((player: any) => (
          <li key={player.id}>
            <strong>ID:</strong> {player.id}, <strong>Nombre:</strong>{" "}
            {player.name}, <strong>Wallet:</strong> {player.wallet},{" "}
            <strong>Conectado:</strong> {player.connected ? "Sí" : "No"}
          </li>
        ))}
      </ul>
    </div>
  );
}

export { PlayerList };
