import GroupComponent from "../components/Navbar";
import ChatBoard from "../components/ChatBoard";
import styles from "./Root.module.css";
import toast from "react-hot-toast";
import React from "react";
import { useState } from "react";
import {
  AppendableUserComponent,
  AppendableAIComponent,
} from "../components/ChatBoard";

const Root = () => {
  //enter key to send message
  document.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      if (document.getElementById("InputField").value !== "") {
        sendMessage();
      }
    }
  });

  const [messageComponents, setMessageComponents] = useState([]);

  const sendMessage = () => {
    //check if input field is empty
    const input = document.getElementById("InputField");
    if (input.value === "") {
      toast.error("Please enter a question", { duration: 3000 });
      return;
    }

    const session_id = localStorage.getItem("session");
    const question = input.value;

    //clear the input field
    input.value = "";

    AppendableUserComponent(question, setMessageComponents);

    toast.loading("Analyzing...");

    fetch("https://api.askpdf.bytespot.tech/chat/" + session_id + "?&q=" + question, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        session_id: session_id,
      },
    })
      .then((response) => response.json())
      .then((result) => {
        if (result["success"] === true) {
          toast.dismiss();
          AppendableAIComponent(result["a"], setMessageComponents);
        } else if (result["success"] === false) {
          toast.dismiss();
          toast.error("Error: " + result["message"], { duration: 3000 });
        }
      })
      .catch((error) => {
        toast.dismiss();
        toast.error("Error: " + error, { duration: 3000 });
      });
  };

  return (
    <div className={styles.root}>
      <GroupComponent />
      <ChatBoard messageComponents={messageComponents} />
      <div className={styles.InputField}>
        <input
          id="InputField"
          disabled
          type="text"
          name="question"
          placeholder="Ask Question"
          className={styles.InputArea}
        />
        <img
          onClick={sendMessage}
          id="SendButton"
          className={styles.InputSubmit}
          loading="lazy"
          alt=""
          src="send.svg"
        />
      </div>
    </div>
  );
};

export default Root;
