package cmd

import "github.com/spf13/cobra"

var runCmd = &cobra.Command{
	Use:   "check",
	Short: "Perform safety checks",
	Run:   doRun,
}

func init() {
	rootCmd.AddCommand(runCmd)
}

func doRun(cmd *cobra.Command, args []string) {
}
