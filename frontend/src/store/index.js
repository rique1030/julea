import { createSlice } from "@reduxjs/toolkit";
import { useDispatch } from "react-redux";
export const ProcessStatus = Object.freeze({
  STOPPED: "stopped",
  RUNNING: "running",
  PAUSED: "paused",
});

const automationStateSlice = createSlice({
  name: "automation",
  initialState: {
    automation: ProcessStatus.STOPPED,
  },
  reducers: {
    setAutomation: (state, action) => {
      state.automation = action.payload;
    },
  },
});

const apiSlice = createSlice({
  name: "api",
  initialState: {
    automation: null,
  },
  reducers: {
    setAutomation: (state, action) => {
      state.automation = action.payload;
    },
  },
});

const outputSlice = createSlice({
  name: "output",
  initialState: {
    output: {},
  },
  reducers: {
    setOutput: (state, action) => {
      state.output = action.payload;
    },
  },
});

const webselectionSlice = createSlice({
  name: "webselection",
  initialState: {
    webselection: {
      chinese: {
        "easy.baidu.com": false,
        "baike.baidu.com": false,
        "qcckyc.com": false,
      },

      euroamerican: {
        "northdata.com": false,
        "avoxdata.com": false,
        "opencorporates.com": false,
        "dnb.com": false,
      },
      shared: {
        "google.com": false,
      },
    },
  },
  reducers: {
    setWebselection: (state, action) => {
      state.webselection = action.payload;
    },
  },
});

const searchMethodSlice = createSlice({
  name: "searchmethod",
  initialState: {
    searchmethod: {
      searchmethod: "single",
      single: "",
      bulk: [],
    },
  },
  reducers: {
    setSearchmethod: (state, action) => {
      state.searchmethod = action.payload;
    },
  },
});

const progressInfoSlice = createSlice({
  name: "progress",
  initialState: {
    progress: {
      site: "",
      progress: 0.0,
      process_info: "",
      status: "",
    },
  },
  reducers: {
    setProgress: (state, action) => {
      state.progress = action.payload;
    },
  },
});

export const { setAutomation } = apiSlice.actions;
export const apiReducer = apiSlice.reducer;

export const { setOutput } = outputSlice.actions;
export const outputReducer = outputSlice.reducer;

export const { setWebselection } = webselectionSlice.actions;
export const webselectionReducer = webselectionSlice.reducer;

export const { setSearchmethod } = searchMethodSlice.actions;
export const searchMethodReducer = searchMethodSlice.reducer;

export const { setAutomationState } = automationStateSlice.actions;
export const automationStateReducer = automationStateSlice.reducer;

export const { setProgress } = progressInfoSlice.actions;
export const progressInfoReducer = progressInfoSlice.reducer;
