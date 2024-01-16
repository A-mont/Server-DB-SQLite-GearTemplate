import { Center } from "@chakra-ui/react";
import { PlayerForm } from "./Server";
import { PlayerList } from "./PlayerList";

function Home() {
  return (
    <Center>
      <PlayerForm />
      <PlayerList/>
    </Center>
  );
}

export { Home };
