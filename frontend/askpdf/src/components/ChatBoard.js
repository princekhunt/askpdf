import styles from "./ChatBoard.module.css";
import { useRef, useEffect } from "react";

// This function is used to append a user message to the chat board.
export function AppendableUserComponent(message, setMessage) {
  const FrameComponent = () => (
    <div className={styles.Frame}>
      <div className={styles.FrameImage}>
        <img className={styles.Image} loading="lazy" alt="" src="user.png" />
      </div>
      <div className={styles.FrameContent}>{message}</div>
    </div>
  );
  const timestamp = new Date().getTime();
  setMessage((previousMessages) => [
    ...previousMessages,
    <FrameComponent key={timestamp} />,
  ]);
}

// This function is used to append an AI message to the chat board.
export function AppendableAIComponent(message, setMessage) {
  const FrameComponent = () => (
    <div className={styles.Frame}>
      <div className={styles.FrameImage}>
        <img className={styles.Image} loading="lazy" alt="" src="askpdf.png" />
      </div>
      <div className={styles.FrameContent}>{message}</div>
    </div>
  );
  const timestamp = new Date().getTime();
  setMessage((previousMessages) => [
    ...previousMessages,
    <FrameComponent key={timestamp} />,
  ]);
}

const ChatBoard = ({ messageComponents }) => {
  
  //scroll to bottom
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };
  useEffect(() => {
    scrollToBottom();
  }, [messageComponents]);

  return (
    <section id="board" className={styles.board}>
      <div id="boardchild" className={styles.boardchild}>
        {/* Message */}
        {messageComponents.map((Component, index) => (
          <div key={index}>{Component}</div>
        ))}

        <div ref={messagesEndRef} />
      </div>
    </section>
  );
};

export default ChatBoard;
