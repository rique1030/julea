import logo from "@assets/images/julea.png";
import styles from "./index.module.css";
import { Link } from "react-router-dom";

function WelcomePage() {
   return (
      <div className={styles.WelcomePage}>
         <div className={styles.InfoContainer}>
            <div className={styles.AppLogoContainer}>
               <img src={logo} className={styles.AppLogo} alt="logo" />
            </div>
            <div className={`${styles.Features} Card`}>
               <div style={{ textAlign: "center" }}>
                  <h1>J.U.L.E.A</h1>
                  <p>Justified & Understanding Legal Entity Assistant</p>
               </div>
               <hr />
               <h4>Key Features</h4>
               <ul>
                  <li>Scrapes different hardcoded sites</li>
                  <li>Quick company existence check</li>
                  <li>Raw results, no guessing</li>
               </ul>
               <hr />
               <Link to="/controller">
                  <button className={styles.StartAutomation}>Start</button>
               </Link>
            </div>
         </div>
         <div className={`${styles.Disclaimer} Card`}>
            <h4>Legal Notice</h4>
            <p>
               JULEA does not replace legal advice or official government
               verification. Use it for internal or technical evaluation only.
               Always verify results from authoritative sources.
            </p>
         </div>
      </div>
   );
}

export default WelcomePage;
