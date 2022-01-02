import axios from "axios";

const Server = axios.create({
  baseURL: "http://192.168.29.129:3000",
});

export const getRequest = async ({ endpoint = "/", ...props }) => {
  console.log(props);
  return await Server.get(endpoint, props);
};
