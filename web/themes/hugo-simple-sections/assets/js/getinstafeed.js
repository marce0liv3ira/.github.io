import * as params from "@params";

async function getInstagramToken() {
  try {
    const response = await fetch(params.tokenURL);
    const data = await response.json();
    return data.token;
  } catch (error) {
    console.error("Error fetching token:", error);
    throw error;
  }
}

getInstagramToken()
  .then((token) => {
    const feed = new Instafeed({
      accessToken: token,
      limit: 20,
      template: `
        <div class="col">
          <a href="{{link}}">
            <img class="img-fluid img-fixed" title="{{caption}}" src="{{image}}" />
          </a>
        </div>`,
    });
    feed.run();
  })
  .catch((error) => {
    console.error("Error setting up Instagram feed:", error);
  });
