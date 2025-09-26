window.app = Vue.createApp({
  el: "#vue",
  mixins: [windowMixin],
  delimiters: ["${", "}"],
  data: function () {
    return {
      currencyOptions: ["sat"],
      settingsFormDialog: {
        show: false,
        data: {},
      },

      jobConfigFormDialog: {
        show: false,
        data: {
          name: null,
          description: null,
          minutes: null,
          hours: null,
          day_of_month: null,
          month: null,
          day_of_week: null,
          pay_from_wallet_id: null,
          pay_to: null,
          currency: "sat",
          amount: null,
        },
      },
      jobConfigList: [],
      jobConfigTable: {
        search: "",
        loading: false,
        columns: [
          {
            name: "name",
            align: "left",
            label: "Name",
            field: "name",
            sortable: true,
          },
          {
            name: "description",
            align: "left",
            label: "Description",
            field: "description",
            sortable: true,
          },
          {
            name: "minutes",
            align: "left",
            label: "Minutes",
            field: "minutes",
            sortable: true,
          },
          {
            name: "hours",
            align: "left",
            label: "Hours",
            field: "hours",
            sortable: true,
          },
          {
            name: "day_of_month",
            align: "left",
            label: "Day of month",
            field: "day_of_month",
            sortable: true,
          },
          {
            name: "month",
            align: "left",
            label: "Month",
            field: "month",
            sortable: true,
          },
          {
            name: "day_of_week",
            align: "left",
            label: "Day of week",
            field: "day_of_week",
            sortable: true,
          },
          {
            name: "pay_from_wallet_id",
            align: "left",
            label: "Wallet",
            field: "pay_from_wallet_id",
            sortable: true,
          },
          {
            name: "pay_to",
            align: "left",
            label: "Pay to",
            field: "pay_to",
            sortable: true,
          },
          {
            name: "currency",
            align: "left",
            label: "Currency",
            field: "currency",
            sortable: true,
          },
          {
            name: "amount",
            align: "left",
            label: "Amount",
            field: "amount",
            sortable: true,
          },
          {
            name: "updated_at",
            align: "left",
            label: "Updated At",
            field: "updated_at",
            sortable: true,
          },
          {
            name: "id",
            align: "left",
            label: "ID",
            field: "id",
            sortable: true,
          },
        ],
        pagination: {
          sortBy: "updated_at",
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10,
        },
      },

      jobRunFormDialog: {
        show: false,
        jobConfig: { label: "All Job Config", value: "" },
        data: {},
      },
      jobRunList: [],
      jobRunTable: {
        search: "",
        loading: false,
        columns: [
          {
            name: "name",
            align: "left",
            label: "Job Name",
            field: "name",
            sortable: true,
          },
          {
            name: "success",
            align: "left",
            label: "Success",
            field: "success",
            sortable: true,
          },
          {
            name: "status_text",
            align: "left",
            label: "Status Text",
            field: "status_text",
            sortable: true,
          },
          {
            name: "duration_seconds",
            align: "left",
            label: "Duration Seconds",
            field: "duration_seconds",
            sortable: true,
          },
          {
            name: "payment_hash",
            align: "left",
            label: "Payment Hash",
            field: "payment_hash",
            sortable: true,
          },
          {
            name: "updated_at",
            align: "left",
            label: "Updated At",
            field: "updated_at",
            sortable: true,
          },
          {
            name: "id",
            align: "left",
            label: "ID",
            field: "id",
            sortable: true,
          },
        ],
        pagination: {
          sortBy: "updated_at",
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10,
        },
      },
      dayOfWeekOptions: [
        { label: "Any", value: null },
        { label: "Sunday", value: 0 },
        { label: "Monday", value: 1 },
        { label: "Tuesday", value: 2 },
        { label: "Wednesday", value: 3 },
        { label: "Thursday", value: 4 },
        { label: "Friday", value: 5 },
        { label: "Saturday", value: 6 },
      ],
      monthOptions: [
        { label: "Any", value: null },
        { label: "January", value: 1 },
        { label: "February", value: 2 },
        { label: "March", value: 3 },
        { label: "April", value: 4 },
        { label: "May", value: 5 },
        { label: "June", value: 6 },
        { label: "July", value: 7 },
        { label: "August", value: 8 },
        { label: "September", value: 9 },
        { label: "October", value: 10 },
        { label: "November", value: 11 },
        { label: "December", value: 12 },
      ],
      dayOfMonthOptions: [
        { label: "Any", value: null },
        ...Array.from({ length: 31 }, (_, i) => ({
          label: (i + 1).toString(),
          value: i + 1,
        })),
      ],
      hourOptions: [
        { label: "Any", value: null },
        ...Array.from({ length: 24 }, (_, i) => ({
          label: i.toString(),
          value: i,
        })),
      ],
      minuteOptions: [
        { label: "Any", value: null },
        ...Array.from({ length: 60 }, (_, i) => ({
          label: i.toString(),
          value: i,
        })),
      ],
    };
  },
  watch: {
    "jobConfigTable.search": {
      handler() {
        const props = {};
        if (this.jobConfigTable.search) {
          props["search"] = this.jobConfigTable.search;
        }
        this.getJobConfig();
      },
    },
    "jobRunTable.search": {
      handler() {
        const props = {};
        if (this.jobRunTable.search) {
          props["search"] = this.jobRunTable.search;
        }
        this.getJobRun();
      },
    },
    "jobRunFormDialog.jobConfig.value": {
      handler() {
        const props = {};
        if (this.jobRunTable.search) {
          props["search"] = this.jobRunTable.search;
        }
        this.getJobRun();
      },
    },
  },

  methods: {
    //////////////// Settings ////////////////////////
    async updateSettings() {
      try {
        const data = { ...this.settingsFormDialog.data };

        await LNbits.api.request("PUT", "/repay/api/v1/settings", null, data);
        this.settingsFormDialog.show = false;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },
    async getSettings() {
      try {
        const { data } = await LNbits.api.request(
          "GET",
          "/repay/api/v1/settings",
          null,
        );
        this.settingsFormDialog.data = data;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },
    async showSettingsDataForm() {
      await this.getSettings();
      this.settingsFormDialog.show = true;
    },

    //////////////// Job Config ////////////////////////
    async showNewJobConfigForm() {
      this.jobConfigFormDialog.data = {
        name: null,
        description: null,
        minutes: null,
        hours: null,
        day_of_month: null,
        month: null,
        day_of_week: null,
        pay_from_wallet_id: null,
        pay_to: null,
        currency: "sat",
        amount: null,
      };
      this.jobConfigFormDialog.show = true;
    },
    async showEditJobConfigForm(data) {
      this.jobConfigFormDialog.data = { ...data };
      this.jobConfigFormDialog.show = true;
    },
    async saveJobConfig() {
      try {
        const data = { extra: {}, ...this.jobConfigFormDialog.data };
        const method = data.id ? "PUT" : "POST";
        const entry = data.id ? `/${data.id}` : "";
        await LNbits.api.request(
          method,
          "/repay/api/v1/job_config" + entry,
          null,
          data,
        );
        this.getJobConfig();
        this.jobConfigFormDialog.show = false;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },

    async getJobConfig(props) {
      try {
        this.jobConfigTable.loading = true;
        const params = LNbits.utils.prepareFilterQuery(
          this.jobConfigTable,
          props,
        );
        const { data } = await LNbits.api.request(
          "GET",
          `/repay/api/v1/job_config/paginated?${params}`,
          null,
        );
        this.jobConfigList = data.data;
        this.jobConfigTable.pagination.rowsNumber = data.total;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      } finally {
        this.jobConfigTable.loading = false;
      }
    },
    async deleteJobConfig(jobConfigId) {
      await LNbits.utils
        .confirmDialog("Are you sure you want to delete this Job Config?")
        .onOk(async () => {
          try {
            await LNbits.api.request(
              "DELETE",
              "/repay/api/v1/job_config/" + jobConfigId,
              null,
            );
            await this.getJobConfig();
          } catch (error) {
            LNbits.utils.notifyApiError(error);
          }
        });
    },
    async exportJobConfigCSV() {
      await LNbits.utils.exportCSV(
        this.jobConfigTable.columns,
        this.jobConfigList,
        "job_config_" + new Date().toISOString().slice(0, 10) + ".csv",
      );
    },

    async getJobRun(props) {
      try {
        this.jobRunTable.loading = true;
        let params = LNbits.utils.prepareFilterQuery(this.jobRunTable, props);
        const jobConfigId = this.jobRunFormDialog.jobConfig.value;
        if (jobConfigId) {
          params += `&job_config_id=${jobConfigId}`;
        }
        const { data } = await LNbits.api.request(
          "GET",
          `/repay/api/v1/job_run/paginated?${params}`,
          null,
        );
        this.jobRunList = data.data;
        this.jobRunTable.pagination.rowsNumber = data.total;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      } finally {
        this.jobRunTable.loading = false;
      }
    },
    async deleteJobRun(jobRunId) {
      await LNbits.utils
        .confirmDialog("Are you sure you want to delete this Job Run?")
        .onOk(async () => {
          try {
            await LNbits.api.request(
              "DELETE",
              "/repay/api/v1/job_run/" + jobRunId,
              null,
            );
            await this.getJobRun();
          } catch (error) {
            LNbits.utils.notifyApiError(error);
          }
        });
    },

    async exportJobRunCSV() {
      await LNbits.utils.exportCSV(
        this.jobRunTable.columns,
        this.jobRunList,
        "job_run_" + new Date().toISOString().slice(0, 10) + ".csv",
      );
    },

    //////////////// Utils ////////////////////////
    dateFromNow(date) {
      return moment(date).fromNow();
    },
    async fetchCurrencies() {
      try {
        const response = await LNbits.api.request("GET", "/api/v1/currencies");
        this.currencyOptions = ["sat", ...response.data];
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },
  },
  ///////////////////////////////////////////////////
  //////LIFECYCLE FUNCTIONS RUNNING ON PAGE LOAD/////
  ///////////////////////////////////////////////////
  async created() {
    this.fetchCurrencies();
    this.getJobConfig();
    this.getJobRun();
  },
});
