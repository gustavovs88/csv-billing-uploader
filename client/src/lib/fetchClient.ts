const apiDomain = import.meta.env.API_DOMAIN;
class FetchClient {
  private domain: string;
  constructor(domain?: string) {
    if (domain) {
      this.domain = domain;
    } else {
      this.domain = "http://localhost:8000";
    }
  }
  async postFile(path = "", file: File) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(`${this.domain}${path}`, {
      method: "POST",
      body: formData,
    });
    return response;
  }
  async get(path = "") {
    const response = await fetch(`${this.domain}${path}`, {
      method: "GET",
    });
    return response.json();
  }
}

export default new FetchClient(apiDomain);
