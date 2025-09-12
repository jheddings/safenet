package main

import (
	"os"

	"github.com/jheddings/safenet/internal/cmd"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/spf13/viper"
)

func init() {
	viper.SetEnvPrefix("SAFENET")
	viper.AutomaticEnv()
	viper.SetConfigFile("safenet.yaml")
	viper.SetConfigType("yaml")

	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			log.Printf("Config file not found; using defaults")
		} else {
			log.Fatal().Err(err).Msgf("Error reading config file: %v", err)
		}
	}

	zerolog.SetGlobalLevel(zerolog.InfoLevel)
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})
}

func main() {
	cmd.Execute()
}
