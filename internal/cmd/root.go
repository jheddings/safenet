package cmd

import (
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var rootCmd = &cobra.Command{
	Use:              "safenet",
	Short:            "SafeNet is a tool for checking the security of your network.",
	PersistentPreRun: initLogging,
}

func init() {
	pFlags := rootCmd.PersistentFlags()

	pFlags.CountP("verbose", "v", "Increase verbosity in logging")
	viper.BindPFlag("verbose", pFlags.Lookup("verbose"))

	pFlags.BoolP("quiet", "q", false, "Only log errors and warnings (override verbose)")
	viper.BindPFlag("quiet", pFlags.Lookup("quiet"))
}

func initLogging(cmd *cobra.Command, args []string) {
	verbose, _ := cmd.Flags().GetCount("verbose")
	quiet, _ := cmd.Flags().GetBool("quiet")

	if quiet {
		zerolog.SetGlobalLevel(zerolog.ErrorLevel)
	} else if verbose > 2 {
		zerolog.SetGlobalLevel(zerolog.TraceLevel)
	} else if verbose > 1 {
		zerolog.SetGlobalLevel(zerolog.DebugLevel)
	} else if verbose > 0 {
		zerolog.SetGlobalLevel(zerolog.InfoLevel)
	} else {
		zerolog.SetGlobalLevel(zerolog.WarnLevel)
	}
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		log.Fatal().Err(err).Msg("Failed to execute root command")
	}
}
