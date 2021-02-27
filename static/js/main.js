function initFingerprintJS() {
    console.debug("Fingerprint init")
    window.visitorIdInit = true
    FingerprintJS.load().then(fp => {
      // The FingerprintJS agent is ready.
      // Get a visitor identifier when you'd like to.
      fp.get().then(result => {
        // This is the visitor identifier:
        const visitorId = result.visitorId;
        console.debug(visitorId);
        window.visitorId = visitorId
      });
    });
  }