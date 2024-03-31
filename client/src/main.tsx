import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import * as Components from "./components";
import { FileProvider } from "./components/ui/file";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      {
        <>
          <Components.Header />
          <FileProvider>
            <Components.FileUploader label="Insira o arquivo csv"></Components.FileUploader>
            <Components.FileListTable />
          </FileProvider>
        </>
      }
    </BrowserRouter>
  </React.StrictMode>
);
