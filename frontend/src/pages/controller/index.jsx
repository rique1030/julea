import styles from "./index.module.css";
import MainPanel from "./main";
import OutputPanel from "./output";
import ControlsPanel from "./controls";
import { useState } from "react";

function ControllerPage() {
   return (
      <div className={styles.ControllerPage}>
         <div className={styles.ControllerConfigContainer}>
            <MainPanel />
            <OutputPanel />
         </div>
         <ControlsPanel />
      </div>
   );
}

export default ControllerPage;
