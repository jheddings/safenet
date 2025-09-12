package cmd

import (
	"os"

	"github.com/jheddings/safenet/internal/target"
	"github.com/pterm/pterm"
	"github.com/rs/zerolog/log"
	"github.com/spf13/cobra"
)

type CheckResult struct {
	Target target.Target
	Safe   bool
	Error  error
}

var checkResults []CheckResult

var runCmd = &cobra.Command{
	Use:   "check",
	Short: "Perform safety checks",
	Run:   doRun,
}

func init() {
	rootCmd.AddCommand(runCmd)
}

func doRun(cmd *cobra.Command, args []string) {

	// check all websites
	for _, website := range cfg.Websites {
		checkTarget(&website)
	}

	// Example: Print all system targets
	for _, system := range cfg.Systems {
		log.Debug().
			Str("name", system.Name).
			Str("address", system.Address).
			Bool("safe", system.Safe).
			Msg("System target")
	}

	// Example: Print all network targets
	for _, network := range cfg.Networks {
		log.Debug().
			Str("name", network.Name).
			Str("network", network.Network).
			Str("address", network.Address).
			Int("port", network.Port).
			Bool("safe", network.Safe).
			Msg("Network target")
	}

	// TODO add a flag to exit with status error
	checkExit()
}

func checkTarget(target target.Target) {
	safe, err := target.Check()

	checkResults = append(checkResults, CheckResult{Target: target, Safe: safe, Error: err})

	if err != nil {
		log.Error().Err(err).Msg("error checking target")
		return
	}

	log.Info().Bool("check", safe).Str("target", target.GetName()).Msg("target check complete")

	if safe {
		pterm.Info.Println(target.GetName(), "is", "safe")
	} else {
		pterm.Error.Println(target.GetName(), "is", "unsafe")
	}
}

func checkExit() {
	errors := 0

	for _, result := range checkResults {
		if !result.Safe {
			errors++
		}
	}

	if errors > 0 {
		os.Exit(1)
	}
}
