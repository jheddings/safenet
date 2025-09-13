package target

import (
	"time"

	probing "github.com/prometheus-community/pro-bing"
	"github.com/rs/zerolog/log"
)

type SystemTarget struct {
	Name    string
	Address string
	Safe    bool
}

// return a friendly name for the target
func (t *SystemTarget) GetName() string {
	return t.Name
}

// check the system for safety
func (t *SystemTarget) Check() (bool, error) {
	log.Debug().Str("name", t.Name).Str("address", t.Address).Bool("safe", t.Safe).Msg("checking system")

	available, err := t.isAvailable()

	// for safe systems: return true if available
	// for unsafe systems: return true if unavailable
	return t.Safe == available, err
}

// determine if the system is available
func (t *SystemTarget) isAvailable() (bool, error) {
	log.Trace().Str("address", t.Address).Msg("PING")

	pinger, err := probing.NewPinger(t.Address)
	if err != nil {
		log.Error().Err(err).Str("name", t.Name).Msg("error creating pinger")
		return false, err
	}

	// XXX make these configurable?
	pinger.Count = 3
	pinger.TTL = 64
	pinger.Size = 56
	pinger.Timeout = 5 * time.Second

	err = pinger.Run()
	if err != nil {
		log.Error().Err(err).Str("name", t.Name).Msg("error running pinger")
		return false, err
	}

	stats := pinger.Statistics()

	log.Debug().Str("name", t.Name).
		Int("packets_sent", stats.PacketsSent).
		Int("packets_recv", stats.PacketsRecv).
		Float64("packet_loss", stats.PacketLoss).
		Msg("packet statistics")

	log.Debug().Str("name", t.Name).
		Dur("min", stats.MinRtt).
		Dur("max", stats.MaxRtt).
		Dur("avg", stats.AvgRtt).
		Msg("ping time")

	available := stats.PacketsRecv > 0
	return available, nil
}
