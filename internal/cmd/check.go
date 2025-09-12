package cmd

import (
	"github.com/rs/zerolog/log"
	"github.com/spf13/cobra"
)

var runCmd = &cobra.Command{
	Use:   "check",
	Short: "Perform safety checks",
	Run:   doRun,
}

func init() {
	rootCmd.AddCommand(runCmd)
}

func doRun(cmd *cobra.Command, args []string) {
	// Example usage of the loaded configuration
	log.Info().Msgf("Loaded %d websites", len(cfg.Websites))
	log.Info().Msgf("Loaded %d systems", len(cfg.Systems))
	log.Info().Msgf("Loaded %d networks", len(cfg.Networks))

	// Example: Print all website targets
	for _, website := range cfg.Websites {
		log.Info().
			Str("name", website.Name).
			Str("address", website.Address).
			Bool("safe", website.Safe).
			Msg("Website target")
	}

	// Example: Print all system targets
	for _, system := range cfg.Systems {
		log.Info().
			Str("name", system.Name).
			Str("address", system.Address).
			Bool("safe", system.Safe).
			Msg("System target")
	}

	// Example: Print all network targets
	for _, network := range cfg.Networks {
		log.Info().
			Str("name", network.Name).
			Str("network", network.Network).
			Str("address", network.Address).
			Int("port", network.Port).
			Bool("safe", network.Safe).
			Msg("Network target")
	}
}
