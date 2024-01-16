import React, { useState } from "react";
import axios from "axios";
import {
  Card,
  CardBody,
  CardHeader,
  Heading,
  Input,
  Button,
  Checkbox,
  Center,
} from "@chakra-ui/react";
import { useAccount } from "@gear-js/react-hooks";


function PlayerForm() {

  const { account, accounts } = useAccount();

  const [formData, setFormData] = useState({
    name: "",
    wallet: "",
    connected: false,
  });

  const handleChange = (e: any) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://localhost:5000/csv_status",
        formData
      );
      console.log(response.data);
    } catch (error) {
      console.error("Error al enviar la solicitud:", error);
    }
  };

  return (
    <Card w="250px" h="500px">
      <CardHeader>
        <Heading size="xl">New Player</Heading>
      </CardHeader>

      <CardBody>
        <form onSubmit={handleSubmit}>
          <Heading size="xl">
            Name:
            <Input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
            />
             
          </Heading>
          <br />
          <Heading size="xl">
            Wallet:
            <Input
              type="text"
              name="wallet"
              value={formData.wallet}
              onChange={handleChange}
            />
            
          </Heading>
          <br />
          <Heading size="xl">
            Connected:
          </Heading>
          <input
              type="checkbox"
              name="connected"
              checked={formData.connected}
              onChange={handleChange}
            />
          <br />
          <Center>
            <Button backgroundColor="green.300" type="submit">
              Registry
            </Button>
          </Center>
        </form>
      </CardBody>
    </Card>
  );
}

export { PlayerForm };
