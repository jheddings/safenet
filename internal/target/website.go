package target

import (
	"net/http"

	"github.com/rs/zerolog/log"
)

type WebsiteTarget struct {
	Name    string
	Address string
	Safe    bool
}

// return a friendly name for the target
func (t *WebsiteTarget) GetName() string {
	return t.Name
}

// check the website for connectivity
func (t *WebsiteTarget) Check() (bool, error) {
	log.Debug().Str("name", t.Name).Str("address", t.Address).Bool("safe", t.Safe).Msg("checking website")

	available, err := t.isAvailable()
	if err != nil {
		return false, err
	}

	// for safe websites: return true if available
	// for unsafe websites: return true if unavailable
	return t.Safe == available, nil
}

// determine if the website is available
func (t *WebsiteTarget) isAvailable() (bool, error) {
	resp, err := http.Get(t.Address)

	if resp != nil {
		log.Trace().Int("status", resp.StatusCode).Str("url", t.Address).Msg("website response status")
		defer resp.Body.Close()
	}

	if err != nil {
		return false, err
	}

	if isHttpStatusOk(resp) {
		return true, nil
	}

	return false, nil
}

// determine if the response is a valid HTTP status
func isHttpStatusOk(resp *http.Response) bool {
	return resp.StatusCode >= 200 && resp.StatusCode < 400
}
