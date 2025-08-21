import styles from "./index.module.css";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { setAutomation, setOutput, setProgress } from "@src/store";
import { ProcessStatus } from "@src/store";
import FlattenSelection from "@src/helpers/flatten_selection.js";

function useAutomation() {
   const searchmethod = useSelector((state) => state.searchmethod.searchmethod);
   const webselection = useSelector((state) => state.webselection.webselection);
   const progress = useSelector((state) => state.progress.progress);

   const dispatch = useDispatch();




   const onPlay = async () => {
      try {
         const status = await window.pywebview.api.get_status();

         if (status === ProcessStatus.PAUSED) {
            await onResume();
            return;
         }
         if (status !== ProcessStatus.STOPPED) {
            console.error("Automation is already running");
            return;
         }

         const selections = FlattenSelection(webselection);
         dispatch(setAutomation(ProcessStatus.RUNNING));
         const search_query = () => {
            if (searchmethod.searchmethod === "single") {
               return [searchmethod.single];
            }
            return searchmethod.bulk;
         }

         if (search_query().length === 0 || selections.length === 0) {
            throw new Error("No search query or website selected");
         }
         const payload = {
            query: {
               site: selections,
               query: search_query()
            },
            cmd: {
               method: "bulk",
               command: "start"
            }

         }
         try {
            const result = await window.pywebview.api.handle_request(payload);
            dispatch(setAutomation(ProcessStatus.STOPPED));
            dispatch(setOutput(result));
         } catch (e) {
            dispatch(setAutomation(ProcessStatus.STOPPED));
         }

      } catch (e) {
         console.log(e);
      }
   };

   const onResume = async () => {
      try {
         const payload = {
            query: {
               site: [],
               query: []
            },
            cmd: {
               method: "bulk",
               command: "resume"
            }

         }
         await window.pywebview.api.handle_request(payload);
         dispatch(setAutomation(ProcessStatus.RUNNING));
      } catch (e) {
         console.log(e);
      }
   };

   const onPause = async () => {
      try {
         const status = await window.pywebview.api.get_status();

         if (status !== ProcessStatus.RUNNING) {
            console.error("Automation is not running");
            return;
         }
         const payload = {
            query: {
               site: [],
               query: []
            },
            cmd: {
               method: "bulk",
               command: "pause"
            }

         }
         await window.pywebview.api.handle_request(payload);
         dispatch(setAutomation(ProcessStatus.PAUSED));
      } catch (e) {
         console.log(e);
      }
   };

   const onStop = async () => {
      try {
         const status = window.pywebview.api.get_status();
         if (status === ProcessStatus.STOPPED) {
            console.error("Automation is not running");
            return;
         }
         const payload = {
            query: {
               site: [],
               query: []
            },
            cmd: {
               method: "bulk",
               command: "stop"
            }

         }
         await window.pywebview.api.handle_request(payload);
         dispatch(setAutomation(ProcessStatus.STOPPED));
      } catch (e) {
         console.log(e);
      }
   };

   const onControlButtonClick = (icon) => {
      switch (icon) {
         case "play_arrow":
            onPlay();
            break;
         case "pause":
            onPause();
            break;
         case "stop":
            onStop();
            break;
         default:
            break;
      }
   };

   useEffect(() => {
      window.setCurrentProgress = (progress) => {
         console.log(progress);
         dispatch(setProgress(progress));
      }
   }, []);

   return {
      progress,
      onControlButtonClick,
   };
}

function ControlsPanel() {
   const { progress, onControlButtonClick } = useAutomation();
   const { site, progress_value, process_info, status } = progress;
   return (
      <div className={`Card ${styles.Controls}`}>
         <div className={styles.ControlsContainer}>
            <p>
               <span style={{ paddingRight: "0.5rem" }}>
                  {site && `[Site: ${site}] `}
               </span>
               {process_info && `[Info: ${process_info}]`}
            </p>
            <ControlButtonSection
               onClick={onControlButtonClick}
               status={status || "stopped"}
            />
         </div>
         <div className={styles.BarBackground}>
            <div
               style={{ width: `calc(99% * ${progress_value || 0})` }}
               className={styles.BarForeground}
            ></div>
         </div>
      </div>
   );
}

function ControlButtonSection({ onClick, status }) {
   return (
      <div className={styles.ControlButtonSection}>
         <ControlButton icon="play_arrow" onClick={onClick} status={status} />
         <ControlButton icon="pause" onClick={onClick} status={status} />
         <ControlButton icon="stop" onClick={onClick} status={status} />
      </div>
   );
}

function ControlButton({ onClick, icon, status }) {
   const green = "var(--rp-moon-pine)";
   const gray = "var(--rp-moon-subtle)";
   const red = "var(--rp-moon-love)";
   const yellow = "var(--rp-moon-gold)";
   const [disabled, setDisabled] = useState(false);
   const [backgroundColor, setBackgroundColor] = useState(gray);

   useEffect(() => {
      let c = gray;
      switch (icon) {
         case "play_arrow":
            if (ProcessStatus.STOPPED == status) {
               c = green;
            }
            if (ProcessStatus.PAUSED == status) {
               c = yellow;
            }
            break;
         case "pause":
            if (ProcessStatus.RUNNING == status) {
               c = yellow;
            }
            break;
         case "stop":
            if (ProcessStatus.STOPPED != status) {
               c = red;
            }
            break;
         default:
            break;
      }
      setDisabled(c == gray);
      setBackgroundColor(c);
   }, [status]);

   return (
      <button
         disabled={disabled}
         onClick={() => onClick(icon)}
         style={{
            "--button-color": backgroundColor,
         }}
         className={styles.ControlButton}
      >
         <i className={`material-icons-outlined`}>{icon}</i>
      </button>
   );
}

export default ControlsPanel;
